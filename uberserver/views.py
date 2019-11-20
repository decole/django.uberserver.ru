from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from uberserver.models import Sensor, Swift


def index(request):
    model = {'title': 'Sensors', 'type_object': 'Index'}
    return render(request, 'pages/main_pages/index.html', model)


def sensors(request):
    sensor_list = Sensor.objects.all()
    model = {'title': 'Sensors', 'type_object': 'sensor', 'sensor_list': sensor_list}
    return render(request, 'pages/sensors/sensors.html', model)


def swifts(request):
    swift_list = Swift.objects.all()
    model = {'title': 'Swifts', 'type_object': 'swift', 'swift_list': swift_list}
    return render(request, 'pages/swifts/swifts.html', model)


def sensor(request, id_sensor):
    sensor_one = Sensor.objects.get(id=id_sensor).get_sensor_data()
    model = {'title': 'Sensor', 'type_object': 'sensor', 'sensor': sensor_one}
    return render(request, 'pages/sensors/sensor.html', model)


def swift(request, id_swift):
    swift_one = Swift.objects.get(id=id_swift).get_swift_data()
    model = {'title': 'Swift', 'type_object': 'swift', 'swift': swift_one}
    return render(request, 'pages/swifts/swift.html', model)
