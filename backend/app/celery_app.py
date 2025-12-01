import os
from celery import Celery

broker = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
backend = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/1')

celery_app = Celery('app', broker=broker, backend=backend)
celery_app.conf.task_routes = {
    'app.tasks.send_reminder_task': {'queue': 'reminders'},
}
