import argparse
import json
import os
import subprocess
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))


def remove_some_dirs_from_path():
    # because there may be a library that interferes with ampy (and actually is)
    dirs_to_remove = []#['lib', 'stabs']
    python_path = os.environ.get('PYTHONPATH', '').split(':')

    for dir_to_remove in dirs_to_remove:
        full_path = os.path.join(ROOT_DIR, dir_to_remove)
        try:
            sys.path.remove(full_path)  
            python_path.remove(full_path)
        except:
            pass
    os.environ['PYTHONPATH'] = ':'.join(python_path)


remove_some_dirs_from_path()


CACHE_FILE_PATH = '/tmp/micropython/uploading_cache.json'
CACHE = {
    'dirs': [],
    'files': {
        'eXaMpLe': 2312312331  # upload timestamp
    }
}


def load_cache():
    global CACHE
    if os.path.isfile(CACHE_FILE_PATH):
        with open(CACHE_FILE_PATH, 'r') as file:
            CACHE = json.load(file)
        print('Cache loaded')
    else:
        print('Cache file not found')


def save_cache():
    global CACHE
    os.makedirs(os.path.dirname(CACHE_FILE_PATH), exist_ok=True)
    with open(CACHE_FILE_PATH, 'w') as file:
        json.dump(CACHE, file)
    print('Cache saved')


def is_ignored_file(file: str):
    if file.endswith('.orig'):
        return True
    if file.endswith('.pyc'):
        return True
    if file in ['__pycache__']:
        return True
    return False


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--port', metavar='PORT', type=str, default='/dev/ttyUSB0',
                        help="Port of the device")
    # parser.add_argument('d', '--delete', action='store_true',
    #                     help='Delete all files on the device instead of uploading')  # not implemented yet...
    parser.add_argument('-f', '--force', action='store_true',
                        help='Upload all files again, even if not modified since caching')

    args = vars(parser.parse_args())
    return args


def run_cmd(cmd):
    output_object = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output_txt = output_object.stdout.decode() + output_object.stderr.decode()
    return output_txt


def _create_dir(args, path):
    if path in CACHE['dirs']:
        print(f'Directory "{path}" already in Cache')
        return

    print(f'Creating directory "{path}"')
    output_txt = run_cmd(f'ampy --port "{args["port"]}" mkdir {path}')
    if output_txt:
        if 'DirectoryExistsError' in output_txt:
            pass
        else:
            print(output_txt)
            raise Exception('Failed to create dir!')
    CACHE['dirs'].append(path)


def _upload_file(args, full_repo_file_path, dev_file_path):
    modification_time = float(os.path.getmtime(full_repo_file_path))
    if CACHE['files'].get(dev_file_path, 0) >= modification_time:
        print(f'File "{dev_file_path}" already in Cache after modification time')
        return

    print(f'# Uploading file "{dev_file_path}"')
    output_txt = run_cmd(f'ampy --port "{args["port"]}" put "{full_repo_file_path}" "{dev_file_path}"')
    if output_txt:
        print(output_txt)
        raise Exception('Failed to upload file!')
    CACHE['files'][dev_file_path] = modification_time


def dev_create_dir(path: str, args, skip_subpaths=True):
    if not path:
        return

    parent_dir = os.path.dirname(path)
    if parent_dir and not skip_subpaths:
        dev_create_dir(path=parent_dir, args=args, skip_subpaths=False)

    _create_dir(args=args, path=path)


def upload_dir(repo_path: str, device_path, args):
    if device_path:
        dev_create_dir(path=device_path, skip_subpaths=False, args=args)
    full_repo_path = os.path.join(ROOT_DIR, repo_path)

    for f in os.listdir(full_repo_path):
        if is_ignored_file(f):
            continue
        full_repo_f_path = os.path.join(full_repo_path, f)
        if os.path.isfile(full_repo_f_path):
            if device_path:
                dev_file_path = os.path.join(device_path, f)
            else:
                dev_file_path = f
            _upload_file(args=args, full_repo_file_path=full_repo_f_path, dev_file_path=dev_file_path)
        else:
            upload_dir(repo_path=os.path.join(repo_path, f),
                       device_path=os.path.join(device_path, f),
                       args=args)


def main(args):
    upload_dir(repo_path='src', device_path='', args=args)
    upload_dir(repo_path='lib', device_path='lib', args=args)


if __name__ == '__main__':
    args = parse_arguments()
    if not args['force']:
        load_cache()
    try:
        main(args)
    finally:
        save_cache()
    print('Finished!')
