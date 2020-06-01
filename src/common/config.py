import ujson
import uos
import machine
import logging

from data_upload.handlers_container import HandlerContainer

MS_TO_S = 1000

cfg = None  # type: ESPConfig
hc = None  # type: HandlerContainer

class ESPConfig:
    def __init__(self):
        self.ssid = ''
        self.password = ''
        self.local_endpoint = ''
        self.aws_endpoint = ''
        self.aws_client_id = ''
        self.aws_topic = ''
        self.data_aqusition_period = 1
        self.data_publishing_period = 1
        self.use_dht = False
        self.use_aws = False
        self.dht_pin = 0
        self.wifi_timeout = 0
        self.mqtt_port = 1883
        self.mqtt_port_ssl = 8883
        self.mqtt_timeout = 0
        self.ap_config_done = False

    def load_from_file(self,):
        file_path = 'config.json'
        with open(file_path, "r", encoding="utf8") as infile:
            config_dict = ujson.load(infile)
            self.ssid = config_dict['ssid']  # TODO: Generic approach to load all data
            self.password = config_dict['password']
            self.local_endpoint = config_dict['local_endpoint']
            self.aws_endpoint = config_dict['aws_endpoint']
            self.aws_client_id = config_dict['client_id']
            self.aws_topic = config_dict['topic']
            self.use_aws = config_dict['use_aws']
            self.data_aqusition_period = config_dict['data_aquisition_period_ms']
            self.data_publishing_period = config_dict['data_publishing_period_s'] * MS_TO_S
            self.use_dht = config_dict['use_dht']
            self.dht_pin = config_dict['dht_pin']
            self.wifi_timeout = config_dict['wifi_connection_timeout']
            self.mqtt_port = config_dict['mqtt_port']
            self.mqtt_port_ssl = config_dict['mqtt_port_ssl']
            self.mqtt_timeout = config_dict['mqtt_timeout']
            self.ap_config_done = config_dict.get('AP_config_done', False)

    def save_to_file(self,):
        file_path = 'config.json'
        config_dict = {}
        config_dict['ssid'] = self.ssid
        config_dict['password'] = self.password
        config_dict['local_endpoint'] = self.local_endpoint
        config_dict['aws_endpoint'] = self.aws_endpoint
        config_dict['client_id'] = self.aws_client_id
        config_dict['topic'] = self.aws_topic
        config_dict['use_aws'] = self.use_aws
        config_dict['data_aquisition_period_ms'] = self.data_aqusition_period
        config_dict['data_publishing_period_s'] = int(self.data_publishing_period / 1000)
        config_dict['use_dht'] = self.use_dht
        config_dict['dht_pin'] = self.dht_pin
        config_dict['wifi_connection_timeout'] = self.wifi_timeout
        config_dict['mqtt_port'] = self.mqtt_port
        config_dict['mqtt_port_ssl'] = self.mqtt_port_ssl
        config_dict['mqtt_timeout'] = self.mqtt_timeout
        config_dict['AP_config_done'] = self.ap_config_done
        with open(file_path, "w", encoding="utf8") as infile:
            ujson.dump(config_dict, infile)
        logging.info("New config saved!")




def init():
    global cfg
    global hc
    hc = HandlerContainer()
    cfg = ESPConfig()
    cfg.load_from_file()
    logging.debug("Configuration loaded")


def print_reset_wake_state():
    reset = machine.reset_cause()
    wake = machine.wake_reason()
    if reset == 1:
        reset = "Power On"
    elif reset == 2:
        reset = "Hard Reset"
    elif reset == 3:
        reset = "Watchdog"
    elif reset == 4:
        reset = "Deepsleep"
    logging.debug("Reset Cause = %s" % reset)
    # TODO: Wake State


def set_ap_config_done(done: bool):
    file_path = 'config.json'
    config_dict = {}
    with open(file_path, "r", encoding="utf8") as infile:
        config_dict = ujson.load(infile)
    config_dict['AP_config_done'] = done
    with open(file_path, "w", encoding="utf8") as infile:
        ujson.dump(config_dict, infile)


def save_current_config():
    global cfg
    file_path = 'config.json'
    with open(file_path, "w", encoding="utf8") as infile:
        ujson.dump(cfg, infile)


def save_network_config(wifi_config: dict):
    file_path = 'config.json'
    config_dict = {}
    with open(file_path, "r", encoding="utf8") as infile:
        config_dict = ujson.load(infile)

    if 'wifi' in wifi_config.keys():
        if 'ssid' in wifi_config['wifi'].keys():
            config_dict['ssid'] = wifi_config['wifi']['ssid']
        if 'password' in wifi_config['wifi'].keys():
            config_dict['password'] = wifi_config['wifi']['password']

    if 'aws' in wifi_config.keys():
        if 'aws_endpoint' in wifi_config['aws'].keys():
            config_dict['aws_endpoint'] = wifi_config['aws']['aws_endpoint']
        if 'client_id' in wifi_config['aws'].keys():
            config_dict['client_id'] = wifi_config['aws']['client_id']
        if 'topic' in wifi_config['aws'].keys():
            config_dict['topic'] = wifi_config['aws']['topic']

    with open(file_path, "w", encoding="utf8") as infile:
        ujson.dump(config_dict, infile)





def save_certificates(config_dict: dict):
    if 'cert_pem' in config_dict.keys():
        cert_str = config_dict['cert_pem']
        cert_path = 'cert/cert.crt'
        try:
            uos.mkdir('cert')
        except:
            # Already exists I can not logging it here
            pass
        with open(cert_path, "w", encoding="utf8") as infile:
            infile.write(cert_str)

    if 'priv_key' in config_dict.keys():
        priv_key = config_dict['priv_key']
        key_path = 'cert/priv.key'
        with open(key_path, "w", encoding="utf8") as infile:
            infile.write(priv_key)


def save_sensor_config(sensor_dict: dict):
    file_path = 'config.json'
    config_dict = {}
    with open(file_path, "r", encoding="utf8") as infile:
        config_dict = ujson.load(infile)

    if 'data_aquisition_period_ms' in sensor_dict.keys():
        config_dict['data_aquisition_period_ms'] = sensor_dict['acquisition_period_ms']
    if 'data_publishing_period_s' in sensor_dict.keys():
        config_dict['data_publishing_period_s'] = sensor_dict['publishing_period_s']

    with open(file_path, "w", encoding="utf8") as infile:
        ujson.dump(config_dict, infile)


