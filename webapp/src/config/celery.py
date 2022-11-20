import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    'send-statistics-every-day-in-7-hour': {
        'task': 'manager.tasks.send_statistics_to_users_email',
        'schedule': crontab(minute='*', hour='*')
    },
# crontab(minute=0, hour=21)
    # 'sweet-sleepyhead': {
    #     'task': 'manager.tasks.send_statistics_to_users_email',
    #     'schedule': crontab()
    # },
}

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     # sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')
#
#     # Calls test('world') every 30 seconds
#     # sender.add_periodic_task(30.0, test.s('world'), expires=10)
#
#     # Executes every Monday morning at 7:30 a.m.
#     sender.add_periodic_task(
#         crontab(hour=7),
#         test.s('Happy Mondays!'),
#     )
#     sender.add_periodic_task(
#         2, send_statistics_to_users_email.s()
#     )


# @app.task
# def test(arg):
#     print(arg)


# @app.task
# def send_statistics_to_users_email():
#     query_set = models.User.objects.filter(email_verify=True)
#     for user in query_set:
#         tasks.send_email_with_statistics.delay(user.email)
