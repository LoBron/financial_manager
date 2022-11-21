import time

from celery import shared_task

from config.celery import app
from users.models import *


@shared_task
def send_email_with_statistics(user_email, use_https=False):
    user = User.objects.get(email=user_email)
    print(f'{user.username} - ты пидрила вонючий')
    current_site = get_current_site(request)
    context = {
        'domain': current_site.domain,
        'site_name': current_site.name,
        'user': user,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_generator.make_token(user),
        'protocol': 'https' if use_https else 'http',
    }
    message = render_to_string('users/verify_email.html', context=context)
    email = EmailMessage('Verify Email', message, to=[user.email])
    email.send()

@app.task
def send_statistics_to_users_email():
    print('-------------- НАЧИНАЮ СПАМ ----------------')
    query_set = User.objects.filter(email_verify=True)
    print(len(query_set))
    for user in query_set:
        send_email_with_statistics.delay(user.email)

