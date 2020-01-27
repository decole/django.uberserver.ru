from uberserver_django.settings import env
from .base_worker import BaseWorker
from ..helpers.email_helper import send_email
from ..models import NotifyMessage


# Воркер вызывается функцией run
# Происходит работа по отправке почтовых сообщений
class EmailWorker(BaseWorker):
    @staticmethod
    def __send(message):
        send_email('почтовая рассылка <email_worker>', message, env.str('NOTIFY_EMAILS'))

    @staticmethod
    def __get_scope():
        # scope = NotifyMessage.objects.get()
        return NotifyMessage.objects.filter(profile_notify='EM', done=False).order_by('id')[:2]

    def run(self):
        scope = self.__get_scope()
        for work in scope:
            self.__send(work.text)
            model = NotifyMessage.objects.get(pk=work.pk)
            model.done = True
            model.save()
        return True
