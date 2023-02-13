import json
import logging
import os
from threading import Lock
import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)


class ConfigAppMeta(type):

    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class ConfigApp(metaclass=ConfigAppMeta):

    __configData: dict = {}

    def __init__(self) -> None:
        path_file: str
        try:
            path_file = os.environ['CONFIG_FILE_TAIXBACKUP']
            with open(path_file, 'r') as config_file:
                self.__configData = json.load(config_file)
        except KeyError:
            logger.error('No se ha definido la variable de entorno CONFIG_FILE_TAIXTRACKING')
        except FileNotFoundError:
            logger.error(f'No se encuentra el fichero de configuración "{path_file}"')

    def get_value(self, first_element: str, second_element: str, default='') -> str:
        try:
            return self.__configData[first_element][second_element]
        except KeyError:
            logger.info(f'No se encuentra el elemento de configuración "{first_element}=>{second_element}"')
            return default

    def get_value_integer(self, first_element: str, second_element: str, default=0) -> int:
        try:
            return self.__configData[first_element][second_element]
        except KeyError:
            logger.info(f'No se encuentra el elemento de configuración "{first_element}=>{second_element}"')
            return default

    def get_value_boolean(self, first_element: str, second_element: str, default=False) -> bool:
        try:
            return self.__configData[first_element][second_element]
        except KeyError:
            logger.info(f'No se encuentra el elemento de configuración "{first_element}=>{second_element}"')
            return default

    def get_client_mqtt(self) -> mqtt.Client:
        client: mqtt.Client = None
        if self.get_value_boolean('mqtt', 'enabled'):
            logger.debug(f"Se conecta el cliente MQTT 'TaixBackups' contra el servidor "
                         f"{self.get_value('mqtt', 'server')}")
            client = mqtt.Client('TaixBackups')
            client.username_pw_set(username=self.get_value('mqtt', 'username'),
                                   password=self.get_value('mqtt', 'password'))
            client.connect(self.get_value('mqtt', 'server'))
        return client
