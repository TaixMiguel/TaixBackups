#!/usr/bin/python3

import json


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

    def add_identifier(self, identifier: str):
        self.__identifiers.append(identifier)

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


def create_sensor(mqtt_device: MQTTDevice, name: str, state_topic: str, object_id: str = "",
                  retain: bool = False) -> MQTTEntity:
    return MQTTEntity(mqtt_device=mqtt_device, name=name, state_topic=state_topic, object_id=object_id, retain=retain)
