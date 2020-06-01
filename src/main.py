import logging
import network
import utime

from web_server import web_app


def configure_access_point(ssid, password):
    ap_handler = network.WLAN(network.AP_IF)
    ap_handler.active(True)
    ap_handler.config(essid="Wizzdev AP", password="")

    interface_config = ap_handler.ifconfig()
    print('ap_if_config: ' + str(interface_config))


def configure_sta(ssid, password):
    sta_handler = network.WLAN(network.STA_IF)
    sta_handler.active(True)
    existing_networks = sta_handler.scan()
    print(existing_networks)

    try:
        sta_handler.connect(ssid, password)
    except:
        return False
    return sta_handler.isconnected()


def main():
    configure_access_point("Wizzdev AP", "")
    web_app.run()

if __name__ == '__main__':
    main()
