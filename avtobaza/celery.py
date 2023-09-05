from __future__ import absolute_import, unicode_literals
import os
import logging
from django.conf import settings

from celery import Celery
from celery.schedules import crontab


logger = logging.getLogger("Celery")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'avtobaza.settings')

app = Celery('avtobaza')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

if not settings.DEBUG:
    app.conf.update(
        BROKER_URL='redis://:{password}@redis:6379/0'.format(password=os.getenv("REDIS_PASSWORD")),
        CELERY_RESULT_BACKEND='redis://:{password}@redis:6379/1'.format(password=os.getenv("REDIS_PASSWORD")),
        CELERY_DISABLE_RATE_LIMITS=True,
        CELERY_ACCEPT_CONTENT=['json', ],
        CELERY_TASK_SERIALIZER='json',
        CELERY_RESULT_SERIALIZER='json',
        CELERY_IMPORTS = ("apps.account.tasks",)
    )
else:
    app.conf.update(
        BROKER_URL='redis://:{password}@redis:6379/0'.format(password="EJZKK7foRij2rxTA"),
        CELERY_RESULT_BACKEND='redis://:{password}@redis:6379/1'.format(password="EJZKK7foRij2rxTA"),
        CELERY_DISABLE_RATE_LIMITS=True,
        CELERY_ACCEPT_CONTENT=['json', ],
        CELERY_TASK_SERIALIZER='json',
        CELERY_RESULT_SERIALIZER='json',
        CELERY_IMPORTS = ("apps.account.tasks",)
    )

app.conf.beat_schedule = {
    'check_user_last_login_time': {
        'task': 'apps.account.tasks.check_user_last_login_time',
        'schedule': crontab(hour='*/6'),
    }
}
