# Хелпер для работы с нотификациями
from uberserver.helpers.telegram_helper import send_telegram_message
from uberserver.models import NotifyProfile, NotifyMessage

'''
Существует всего 3 типа нотификаций:
1. email (email)
2. telegram (telegram bot)
3. site (notification on popup in site)
'''


def send_notify(profile, message):
    if profile == 'email':
        profile_id = NotifyProfile.objects.get(name='email').external_id
        NotifyMessage(profile_id=profile_id, text=message).save()
    if profile == 'telegram':
        profile_id = NotifyProfile.objects.get(name='telegram_bot').external_id
        NotifyMessage(profile_id=profile_id, text=message).save()
    if profile == 'site':
        profile_id = NotifyProfile.objects.get(name='site_notify').external_id
        NotifyMessage(profile_id=profile_id, text=message).save()


def notify(profile, message):
    if isinstance(profile, list):
        for profile_type in profile:
            send_notify(profile_type, message)

    if isinstance(profile, str):
        send_notify(profile, message)
