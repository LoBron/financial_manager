import time

from celery import shared_task
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from config.celery import app
from manager.models import *
from .utils import check_balance, get_user_statistics
from users.models import *


@shared_task
def send_email_with_statistics(user_email):
    user = User.objects.get(email=user_email)
    context = {
        'statistics': get_user_statistics(user.pk),
        'balance': check_balance(user.pk),
        'user': user,
    }
    message = render_to_string('manager/user_statistics.html', context=context)
    email = EmailMessage('User statistics', message, to=[user.email])
    email.send()


@app.task
def distribution_of_tasks_for_sending_statistics():
    query_set = User.objects.filter(email_verify=True)
    for user in query_set:
        send_email_with_statistics.delay(user.email)
