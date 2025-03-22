from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json

# Create an interval schedule (run every day)
schedule, created = IntervalSchedule.objects.get_or_create(
    every=1,
    period=IntervalSchedule.DAYS
)

# Create a periodic task for sending reminders
PeriodicTask.objects.get_or_create(
    interval=schedule,
    name="Send Ticket Reminders",
    task="support.tasks.send_ticket_reminders",
    defaults={"args": json.dumps([])}
)
