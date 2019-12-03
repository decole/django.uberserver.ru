# manage.py mqtt - starting command
# pip install paho-mqtt
from django.core.management.base import BaseCommand, CommandError
from uberserver_django.settings import env
import paho.mqtt.client as mqtt
import requests
import json
# https://github.com/eclipse/paho.mqtt.python/blob/master/examples/client_sub-class.py


class MicroMQTTClass(mqtt.Client):

    def on_connect(self, mqttc, obj, flags, rc):
        # print("rc: "+str(rc))
        print('connected')

    def on_message(self, mqttc, obj, msg):
        # print(msg.topic+"  "+str(msg.payload.decode()))
        url = env('URI_MQTT_API')
        headers = {
            'Content-type': 'application/json',
        }
        data = {"topic": msg.topic, "payload": msg.payload.decode()}  # , "payload": msg.payload.decode()
        ar = requests.post(url, data=json.dumps(data), headers=headers)
        # print(json.dumps(data))
        # print(ar)
        #  Todo остановить цикл если не приходит код 200 ответ от сайта и кинуть в телегу сообщение о невозможности
        #   отправки

    def on_publish(self, mqttc, obj, mid):
        print("publishing: "+str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def run(self):
        self.connect(env('MQTT_IP'), env.int('MQTT_PORT'), 60)
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
