import utime
import ntptime
import utime
import uos

TIME_EPOCH_SHIFT = 946684800000  # in ms - embedded port of Unix time counts from year 2000, not 1970


def sync_time_with_ntpserver():
    # TODO: check if time was actually synced
    ntptime.settime()  # get current time from ntp server


def get_current_timestamp_ms():
    return int(round(utime.time() * 1000 + (utime.ticks_ms() % 1000) + TIME_EPOCH_SHIFT))


def get_time_str():
    t = utime.ticks_ms()
    return '%.3f' % (t/1000)


def check_file_exists(path_to_file: str):
    return uos.stat(path_to_file)[6]