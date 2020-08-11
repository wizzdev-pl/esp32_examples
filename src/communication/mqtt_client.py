from umqtt.simple import MQTTClient  # micropython-umqtt library


CA_CERT_PATH = "/certs/cacert.pem"
PRIV_KEY_PATH = "/certs/priv.key"
PRIV_KEY_PATH = "/certs/cert.crt"


def read_certificate():
    with open(PRIV_KEY_PATH, 'r') as f:
        key = f.read()

    with open(PRIV_KEY_PATH, 'r') as f:
        cert = f.read()

    return {'key': key, 'cert': cert}


def connect_to_mqtt_broker(client_id, aws_endpoint, key_str, cert_str):
        mqtt_client = MQTTClient(client_id=client_id,
                                           server=aws_endpoint,
                                           port=8883, keepalive=4000,
                                           ssl=True,
                                           ssl_params={
                                                "server_side": False,
                                                "key": key_str,
                                                "cert": cert_str
                                                 })

        mqtt_client.connect()
        return mqtt_client



