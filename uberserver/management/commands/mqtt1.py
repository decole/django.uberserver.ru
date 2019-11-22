# manage.py mqtt - starting command
# pip install paho-mqtt
from django.core.management.base import BaseCommand, CommandError
from uberserver.models import Sensor, Swift
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
   print("Connected With Result Code " (rc))


def on_message_from_sensor(client, userdata, message):
    print('sensor: {topic} - {payload} '.format(topic=message.topic, payload=message.payload.decode()))


def on_message_from_swift(client, userdata, message):
    print('swift {topic} - {payload} '.format(topic=message.topic, payload=message.payload.decode()))


def on_message_from_kitchen(client, userdata, message):
    print("Message Recieved from Restroom: "+message.payload.decode())


def on_message_from_bedroom(client, userdata, message):
    print("Message Recieved from lamp01: "+message.payload.decode())


def on_message(client, userdata, message):
    # print("Message Recieved from Others: "+message.payload.decode())
    pass

# https://mntolia.com/mqtt-python-with-paho-mqtt-client/
class Command(BaseCommand):
    help = 'mqtt client from django app'
    broker_url = "uberserver.ru"
    broker_port = 2223

    def handle(self, *args, **options):
        sensor_list = Sensor.objects.all()
        swift_list = Swift.objects.all()

        client = mqtt.Client()
        client.on_connect = on_connect
        # To Process Every Other Message
        client.on_message = on_message
        client.connect(self.broker_url, self.broker_port)
        client.subscribe("#", qos=1)
        for sensor in sensor_list:
            client.subscribe(str(sensor.topic), qos=1)
        for swift in swift_list:
            client.subscribe(str(swift.topic), qos=1)

        for sensor in sensor_list:
            client.message_callback_add(str(sensor.topic), on_message_from_sensor)
        for swift in swift_list:
            client.message_callback_add(str(swift.topic), on_message_from_swift)

        client.loop_forever()
