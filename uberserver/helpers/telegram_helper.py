from django.conf import settings
import requests


def send_telegram_message(text):
    token = settings.TELEGRAM_TOKEN
    url = "https://api.telegram.org/bot"
    channel_id = "245579764"
    url += token
    method = url + "/sendMessage"
    requests.post(method, data={
        "chat_id": channel_id,
        "text": text
    }, proxies=dict(https=settings.PROXY_SOCKS5))
