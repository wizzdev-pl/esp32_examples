import ure as re
import picoweb
import ulogging as logging
import ujson
import utime

app = picoweb.WebApp(__name__)

# API helpers
def create_success_response(data: dict):
    return _create_common_response(data=data, status=0, status_text='ok')


def _create_common_response(data, status: int, status_text: str):
    response_dict = {
        'data': data,
        'status': status,
        'status_text': status_text,
    }
    encoded = ujson.dumps(response_dict)
    return encoded


def create_failed_response(resp, status_text: str, status: int = 500):
    return _create_common_response(data=None, status=status, status_text=status_text)


# modified picoweb's req.read_form_data:
def parse_post_body(req):
    size = int(req.headers[b"Content-Length"])
    data = yield from req.reader.readexactly(size)
    data_txt = data.decode('utf-8')
    return ujson.loads(data_txt)

# Requests handling
@app.route("/status")
def get_status(req, resp):
    data = {"timestamp": utime.time()}
    data["name"] = "Wizzdev web app"
    data["status"] = "OK"
    encoded = create_success_response(data=data)
    yield from picoweb.start_response(resp, content_type="application/json")
    yield from resp.awrite(encoded)

@app.route("/")
def index(req, resp):
    print("route /")
    headers = {"Location": "/web_pages/index.html"}
    yield from picoweb.start_response(resp, status="303", headers=headers)

@app.route(re.compile("/web_pages/(.+)"))
def get_static_file(req, resp):
    print("Get static call")
    file_path = '/web_server/web_pages/' + req.url_match.group(1)
    logging.info('About to send file: ' + file_path)
    yield from app.sendfile(resp, file_path)

@app.route("/config")
def set_config(req, resp):
    data = yield from parse_post_body(req)
    print(data)

    if 'wifi' in data.keys():
        print(data['wifi'])

    response_data = {'result': 'ok'}
    encoded = create_success_response(data=response_data)
    yield from picoweb.start_response(resp, content_type="application/json")
    yield from resp.awrite(encoded)

@app.route("/name")
def get_name(req, resp):
    data = {"name": "WizzDev ESP32 web app example"}
    encoded = create_success_response(data=data)
    yield from picoweb.start_response(resp, content_type="application/json")
    yield from resp.awrite(encoded)

def run():
    global app

    logging.info('About to start server...')
    app.run(debug=1, port=80, host='0.0.0.0')


def stop_server():
    app.stop_server()
