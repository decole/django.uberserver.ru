import time
import pycron
from django.core import management
from django.core.management.base import BaseCommand
from uberserver.helpers.notify_helper import notify
from uberserver.models import Scheduler


class Command(BaseCommand):
    help = 'Scheduler for cron and DB'

    def handle(self, *args, **options):
        try:
            tasks = Scheduler.objects.all()
            for work in tasks:
                current_task = work.get_scheduler_data()
                now = int(time.time())
                start_date = int(current_task['date_start'].timestamp())
                if current_task["active"] and now > start_date and pycron.is_now(current_task['periodic']):
                    management.call_command(current_task['command'])

        except Exception as e:
            print("Exception (scheduler):", e)
            # create message in Notify table to email, t.bot, site
            notify(['email', 'telegram', 'site'], ("Exception (scheduler):", e))
            pass
