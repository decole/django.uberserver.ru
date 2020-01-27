from .base_worker import BaseWorker
from ..helpers.telegram_helper import send_telegram_message
from ..models import NotifyMessage


class TelegramWorker(BaseWorker):
    @staticmethod
    def __send(message):
        send_telegram_message(str(message))

    @staticmethod
    def __get_scope():
        return NotifyMessage.objects.filter(profile_notify='TE', done=False).order_by('id')[:10]

    def run(self):
        scope = self.__get_scope()
        message = ''
        for work in scope:
            message = message + (work.text + ' ' + work.created_at.strftime("%d.%m.%Y %H:%M:%S") + "\n")
            model = NotifyMessage.objects.get(pk=work.pk)
            model.done = True
            model.save()
        self.__send(message)
        return True
