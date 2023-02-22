#!/usr/bin/python3

import json

from app import kTaixBackups


def add_param_if_not_empty(json_data: str, key: str, data):
    if data:
        json_data[key] = data


class MQTTDevice:

    def __init__(self, manufacturer: str, name: str, model: str, version: str):
        self.__manufacturer = manufacturer
        self.__version = version
        self.__identifiers = []
        self.__model = model
        self.__name = name

    def add_identifier(self, identifier: str) -> None:
        self.__identifiers.append(identifier)

    def get_first_identifier(self) -> str:
        if self.__identifiers:
            return self.__identifiers[0]
        return ''

    def format_json(self) -> dict:
        json_device = {}
        add_param_if_not_empty(json_device, 'identifiers', self.__identifiers)
        add_param_if_not_empty(json_device, 'manufacturer', self.__manufacturer)
        add_param_if_not_empty(json_device, 'sw_version', self.__version)
        add_param_if_not_empty(json_device, 'model', self.__model)
        add_param_if_not_empty(json_device, 'name', self.__name)
        return json_device


class MQTTEntity:
    __mqttDevice: MQTTDevice
    unitOfMeasurement: str = ''
    component: str = 'sensor'
    __commandTopic: str
    __stateTopic: str
    __objectId: str
    __uniqueId: str
    __retain: bool
    icon: str = ''
    __name: str

    def __init__(self, mqtt_device: MQTTDevice, name: str, object_id: str, state_topic: str = '',
                 command_topic: str = '', retain: bool = False):
        self.__mqttDevice = mqtt_device
        self.__stateTopic = state_topic
        self.__commandTopic = command_topic
        self.__objectId = object_id
        self.__uniqueId = object_id
        self.__retain = retain
        self.__name = name

    def format_json(self) -> str:
        json_entity = {'retain': self.__retain}
        add_param_if_not_empty(json_entity, 'icon', self.icon)
        add_param_if_not_empty(json_entity, 'name', self.__name)
        add_param_if_not_empty(json_entity, 'object_id', self.__objectId)
        add_param_if_not_empty(json_entity, 'unique_id', self.__uniqueId)
        add_param_if_not_empty(json_entity, 'state_topic', self.__stateTopic)
        add_param_if_not_empty(json_entity, 'command_topic', self.__commandTopic)
        add_param_if_not_empty(json_entity, 'unit_of_measurement', self.unitOfMeasurement)
        json_entity['device'] = self.__mqttDevice.format_json()
        return json.dumps(json_entity)

    def get_config_topic(self, discovery_prefix: str='homeassistant') -> str:
        first_identifier: str = self.__mqttDevice.get_first_identifier()
        topic: str = discovery_prefix + '/' + self.component + '/'
        if first_identifier:
            topic += first_identifier + '/'
        topic += self.__objectId + '/config'
        return topic


class MQTTTool:

    __backup_name: str
    __mqtt_device: MQTTDevice

    def __init__(self, mqtt_device: MQTTDevice, backup_name: str):
        self.__backup_name = backup_name
        self.__mqtt_device = mqtt_device

    def create_sensor_last_execution(self) -> MQTTEntity:
        state_topic = f'stat{kTaixBackups.MQTT.TOPIC}{self.__backup_name}/lastExecution'
        return create_sensor(mqtt_device=self.__mqtt_device, name=f'Ejecución [{self.__backup_name}]', retain=True,
                             state_topic=state_topic, object_id=f'taixBackups_{self.__backup_name}_lastExecution')

    def create_sensor_state_backup(self) -> MQTTEntity:
        state_topic = f'stat{kTaixBackups.MQTT.TOPIC}{self.__backup_name}/stateBackup'
        return create_sensor(mqtt_device=self.__mqtt_device, name=f'Estado [{self.__backup_name}]', retain=True,
                             state_topic=state_topic, object_id=f'taixBackups_{self.__backup_name}_stateBackup')


def create_sensor(mqtt_device: MQTTDevice, name: str, state_topic: str, object_id: str = "",
                  retain: bool = False) -> MQTTEntity:
    return MQTTEntity(mqtt_device=mqtt_device, name=name, state_topic=state_topic, object_id=object_id, retain=retain)

def create_device() -> MQTTDevice:
    from app import kTaixBackups
    mqtt_device: MQTTDevice = MQTTDevice(manufacturer='TaixMiguel', name=kTaixBackups.APP_NAME, model='TaixBackups',
                                         version=kTaixBackups.APP_VERSION)
    mqtt_device.add_identifier('taixBackup')
    return mqtt_device
