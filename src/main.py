import logging
import utime
import ujson

from web_server import web_app
from communication.wirerless_connection import configure_AP, configure_STA
from communication.mqtt_client import read_certificate, connect_to_mqtt_broker


'''
This example configures an AccessPoint with a simple web server.
After connecting to the 'WizzDev AP' network from another device you will be able to see 
a simple web application at the address 192.168.4.1. 
For available API requests see web_server/web_app.py.
'''
def example_access_point():
    # Configuring the open AccessPoint:
    ap_handler = configure_AP(ssid='WizzDev AP', password='password')

    # Starting the web applicaition:
    web_app.run()



'''
This example connects the ESP32 to an existing WiFi network, and sends single MQTT message.
You must input a valid WiFi network settings, configure AWS IoT core, and download certificates to the device in order to run this example.
All of this was described in blog post on WizzDev's page: https://wizzdev.pl/blog/how-to-send-data-from-iot-device-to-aws-cloud/
'''
def example_sending_mqtt():
    #Configure YOUR WiFI connection
    ssid = 'wifi_ssid'
    password = 'password'
    sta_handler = configure_STA(ssid, password)

    if sta_handler:
        cert_data = read_certificate()                      # make sure the certificate has been created and uploaded to device first!
        aws_endpoint = 'xxxxxxxxxxxxxxxxx.region.amazonaws.com'    # change this to your actual ENDPOINT!

        if sta_handler.isconnected():
            # connect to mqtt broker and send message:
            try:
                mqtt_client = connect_to_mqtt_broker(client_id='blog_test',
                                                     aws_endpoint=aws_endpoint,
                                                     key_str=cert_data['key'],
                                                     cert_str=cert_data['cert'])
            except Exception as e:
                logging.error('Could not connect to MQTT broker! Reason {}'.format(str(e)))
            else:
                message = {'name': 'Myfirst MQTT message', 'id': 1}
                mqtt_client.publish(topic='example', msg=ujson.dumps(message))


def main():
    '''
    Select an example to run and comment the others:
    '''

    # example_access_point()
    example_sending_mqtt()

if __name__ == '__main__':
    main()
