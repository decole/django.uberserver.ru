import datetime
import time
import pycron
from django.core import management
from django.core.management.base import BaseCommand
from uberserver.helpers.notify_helper import notify
from uberserver.models import Scheduler, ScheduleTaskHistory


class Command(BaseCommand):
    help = 'Scheduler for cron and DB'

    def handle(self, *args, **options):
        current = ''
        try:
            tasks = Scheduler.objects.all()
            for work in tasks:
                current_task = work.get_scheduler_data()
                now = int(time.time())
                start_date = int(current_task['date_start'].timestamp())

                if current_task["active"] and now > start_date and pycron.is_now(current_task['periodic']):
                    history = ScheduleTaskHistory()
                    history.task = current = current_task['command']
                    management.call_command(current_task['command'])
                    datetime_now = datetime.datetime.today().strftime("%d.%m.%Y %H:%M:%S")
                    notify(['site'], 'task - ' + current_task['command'] + 'is finished ' + datetime_now)
                    history.state = True
                    history.save()
        except Exception as e:
            history = ScheduleTaskHistory()
            history.task = current
            history.state = False
            history.save()
            print("Exception (scheduler):", e)
            # create message in Notify table to email, t.bot, site
            notify(['email', 'telegram', 'site'], ("Exception (scheduler):", e))
            pass
