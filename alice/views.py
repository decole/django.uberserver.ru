import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from uberserver.helpers.mqtt_helper import analise, get_payload, post_payload


# https://github.com/yandex/alice-skills/blob/master/python/buy-elephant/azure/main.py
@csrf_exempt
def alice_api(request):
    if request.method == 'GET':
        return HttpResponse(json.dumps([{"response": "ok"}, {"method": "GET"}]), content_type="application/json")
    if request.method == 'POST':
        res = json.loads(request.body.decode())
        analise(res)  # функция анализатора
        return HttpResponse(json.dumps([{"response": "ok"}, {"method": "POST"}]), content_type="application/json")


# @csrf_exempt
# def mqtt_api_get(request):
#     if request.method == 'GET':
#         if request.GET.get('topic') is not None:
#             topic = request.GET.get('topic')
#             payload = get_payload(topic)
#             return HttpResponse(
#                 json.dumps([{"topic": topic, "payload": payload}]), content_type="application/json")
#         return HttpResponse(None)
#     if request.method == 'POST':
#         return HttpResponse(None)
#
#
# @csrf_exempt
# def mqtt_api_post(request):
#     if request.method == 'GET':
#         return HttpResponse(None)
#     if request.method == 'POST':
#         topic = request.POST.get('topic')
#         payload = request.POST.get('payload')
#         status = post_payload(topic, payload)
#         return HttpResponse(
#             json.dumps([{"status": status}]), content_type="application/json")
#     return HttpResponse(json.dumps([{"status": "false"}]), content_type="application/json")
#
