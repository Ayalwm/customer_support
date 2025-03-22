import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'customer_support.settings')

app = Celery('customer_support')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
