# Хелпер для работы с нотификациями
from uberserver.models import NotifyMessage

'''
Существует всего 3 типа нотификаций:
1. email (email)
2. telegram (telegram bot)
3. site (notification on popup in site)

Пример вызова нотификации
notify(['site', 'telegram', 'email'], 'task - test notify')
notify('site', 'task - test notify')
'''


def send_notify(profile, message):
    if profile == 'email':
        profile_id = 'EM'
        NotifyMessage(profile_notify=profile_id, text=message).save()
    if profile == 'telegram':
        profile_id = 'TE'
        NotifyMessage(profile_notify=profile_id, text=message).save()
    if profile == 'site':
        profile_id = 'SI'
        NotifyMessage(profile_notify=profile_id, text=message).save()


def notify(profile, message):
    if isinstance(profile, list):
        for profile_type in profile:
            send_notify(profile_type, message)

    if isinstance(profile, str):
        send_notify(profile, message)
