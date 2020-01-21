import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from uberserver.helpers.mqtt_helper import analise, get_payload, post_payload
from uberserver.models import Sensor, Swift
from django.contrib.auth.models import User


def index(request):
    if request.user.is_authenticated:
        model = {'title': 'Sensors', 'type_object': 'Index'}
        return render(request, 'pages/main_pages/index.html', model)
    else:
        return redirect('login')


def sensors(request):
    if request.user.is_authenticated:
        sensor_list = Sensor.objects.all()
        model = {'title': 'Sensors', 'type_object': 'sensor', 'sensor_list': sensor_list}
        return render(request, 'pages/main_pages/sensors.html', model)
    else:
        return redirect('login')


def swifts(request):
    if request.user.is_authenticated:
        swift_list = Swift.objects.all()
        model = {'title': 'Swifts', 'type_object': 'swift', 'swift_list': swift_list}
        return render(request, 'pages/main_pages/swifts.html', model)
    else:
        return redirect('login')


@csrf_exempt
def mqtt_api(request):
    if request.method == 'GET':
        return HttpResponse(json.dumps([{"response": "ok"}, {"method": "GET"}]), content_type="application/json")
    if request.method == 'POST':
        res = json.loads(request.body.decode())
        analise(res)  # функция анализатора
        return HttpResponse(json.dumps([{"response": "ok"}, {"method": "POST"}]), content_type="application/json")


@csrf_exempt
def mqtt_api_get(request):
    if request.method == 'GET':
        if request.GET.get('topic') is not None:
            topic = request.GET.get('topic')
            payload = get_payload(topic)
            return HttpResponse(
                json.dumps([{"topic": topic, "payload": payload}]), content_type="application/json")
        return HttpResponse(None)
    if request.method == 'POST':
        return HttpResponse(None)


@csrf_exempt
def mqtt_api_post(request):
    if request.method == 'GET':
        return HttpResponse(None)
    if request.method == 'POST':
        topic = request.POST.get('topic')
        payload = request.POST.get('payload')
        status = post_payload(topic, payload)
        return HttpResponse(
            json.dumps([{"status": status}]), content_type="application/json")
    return HttpResponse(json.dumps([{"status": "false"}]), content_type="application/json")


def login_page(request):
    model = {'login': ''}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        model = {'login': username}
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            model = {'login': username, 'message': 'логин или пароль не подходят'}
            return render(request, 'adminlte/login.html', model)
    return render(request, 'adminlte/login.html', model)


def register_page(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        model = {'message': 'lol'}
        if request.method == "POST":
            model = {'message': 'post'}
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            if username is '' or email is '' or password is '':
                model = {'message': 'введите полностью все данные'}
                return render(request, 'adminlte/register.html', model)
            else:
                user = User.objects.create_user(username, email, password)
                model = {'succes': 'регистрация прошла успешно'}
                render(request, 'adminlte/as_registered.html', model)

        return render(request, 'adminlte/register.html', model)


def logout_page(request):
    logout(request)
    return redirect('login')
