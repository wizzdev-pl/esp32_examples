import network
import time

MIN_PASSWORD_LENGTH = 8
WIFI_CONNECTION_MAX_NUMBER_OF_RETRIES = 10
WIFI_CONNECTION_CHECK_SLEEP_TIME_S = 1


def configure_AP(ssid, password=None):
    ap_handler = network.WLAN(network.AP_IF)
    ap_handler.active(True)
    if password is None:
        ap_handler.config(essid=ssid)
    else:
        if len(password) < MIN_PASSWORD_LENGTH:
            raise Exception('Password is too short! Min passowrd length is: {}'.format(MIN_PASSWORD_LENGTH))
        ap_handler.config(essid=ssid, authmode=network.AUTH_WPA_WPA2_PSK, password=password)

    interface_config = ap_handler.ifconfig()
    print('ap_if_config: ' + str(interface_config))
    return ap_handler


def configure_STA(ssid, password):
    sta_handler = network.WLAN(network.STA_IF)
    sta_handler.active(True)
    existing_networks = sta_handler.scan()
    print(existing_networks)

    try:
        sta_handler.connect(ssid, password)
    except:
        return None

    number_of_retries_connection = 0

    while not sta_handler.isconnected():
        time.sleep(WIFI_CONNECTION_CHECK_SLEEP_TIME_S)
        number_of_retries_connection += 1
        if number_of_retries_connection >= WIFI_CONNECTION_MAX_NUMBER_OF_RETRIES:
            break

    if sta_handler.isconnected():
        sta_handler.ifconfig()
        return sta_handler
