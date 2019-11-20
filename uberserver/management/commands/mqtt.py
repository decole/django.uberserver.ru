# manage.py mqtt - starting command
from django.core.management.base import BaseCommand, CommandError


import paho.mqtt.subscribe as subscribe


# from uberserver.helpers.mqttHelper import on_message_print
def on_message_print(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))



class Command(BaseCommand):
    help = 'mqtt client from django app'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Mqtt client is starting'))
        subscribe.callback(on_message_print, "#", hostname="192.168.1.5", port=1883)
