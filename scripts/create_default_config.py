import os
import json

PATH_TO_JSON = './src/config.json'

if os.path.exists(PATH_TO_JSON):
    print(f"Config exists at: ", os.path.abspath(PATH_TO_JSON))
    exit(1)
else:
    config_dict = {
        "ssid": "ssid",
        "password": "password",
        "local_endpoint": "",
        "aws_endpoint": "",
        'client_id': "default_id",
        'topic': "default_topic",
        'use_aws': False,
        'data_aquisition_period_ms': 2000,
        'data_publishing_period_s': 20,
        'use_dht': False,
        'dht_pin': 4,
        'wifi_connection_timeout': 5000,  # ms
        'mqtt_port': 1883,
        'mqtt_port_ssl': 8883,
        'mqtt_timeout': 4000,  # ms
        "AP_config_done": False
    }
    with open(PATH_TO_JSON, 'w+') as f:
        f.write(json.dumps(config_dict, indent=4))
        print(f"Default config written to {os.path.abspath(PATH_TO_JSON)}")
        exit(0)
