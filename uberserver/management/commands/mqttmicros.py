# manage.py mqtt - starting command
# pip install paho-mqtt
from django.core.management.base import BaseCommand, CommandError
import paho.mqtt.client as mqtt
import requests
import json


# https://github.com/eclipse/paho.mqtt.python/blob/master/examples/client_sub-class.py
class MyMQTTClass(mqtt.Client):

    def on_connect(self, mqttc, obj, flags, rc):
        # print("rc: "+str(rc))
        print('connected')

    def on_message(self, mqttc, obj, msg):
        print(msg.topic+"  "+str(msg.payload.decode()))
        # url = 'http://127.0.0.1:8000/api/mqtt'
        url = 'http://127.0.0.1:8000/api/mqtt'
        headers = {
            'Content-type': 'application/json',
            # 'charset': 'utf-8'
        }
        data = {"topic": msg.topic, "payload": msg.payload.decode()}  # , "payload": msg.payload.decode()
        print(json.dumps(data))
        ar = requests.post(url, data=json.dumps(data), headers=headers)
        print(ar)


    def on_publish(self, mqttc, obj, mid):
        print("publishing: "+str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def run(self):
        self.connect("192.168.1.5", 1883, 60)
        self.subscribe("#", 0)

        rc = 0
        while rc == 0:
            rc = self.loop()
        return rc


class Command(BaseCommand):
    help = 'mqtt client from django app'

    def handle(self, *args, **options):
        mqttc = MyMQTTClass()
        mqttc.run()
