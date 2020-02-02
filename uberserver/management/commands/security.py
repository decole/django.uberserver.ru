from django.core.management.base import BaseCommand, CommandError

from uberserver.helpers.mqtt_helper import security_analise
from uberserver.models import SecuritySensor
from uberserver_django.settings import env
import paho.mqtt.client as mqtt
import requests
import json
# https://github.com/eclipse/paho.mqtt.python/blob/master/examples/client_sub-class.py


class MicroMQTTClass(mqtt.Client):

    def on_connect(self, mqttc, obj, flags, rc):
        print('connected')

    def on_message(self, mqttc, obj, msg):
        security_analise(json.dumps({"topic": msg.topic, "payload": msg.payload.decode()}))

    def on_publish(self, mqttc, obj, mid):
        print("publishing: "+str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def run(self):
        self.connect(env('MQTT_IP'), env.int('MQTT_PORT'), 60)
        # Todo подписатся на пожарные топики
        # Todo в дальнейшем функционал внедрить в основной процесс считывания топиков
        self.subscribe("#", 0)

        rc = 0
        while rc == 0:
            rc = self.loop()
        return rc


class Command(BaseCommand):
    help = 'mqtt client from django app'

    def handle(self, *args, **options):
        mqttc = MicroMQTTClass()
        mqttc.run()
