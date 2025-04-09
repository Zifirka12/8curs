from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from celery import shared_task
from materials.models import Subscription


@shared_task
def check_course_update(pk):
    subs = Subscription.objects.filter(course_id=pk)

    for s in subs:
        send_mail(subject='Оповещание об обновлении курса',
                  message=f'Курс {s.course.name}, получил изменения !!!',
                  from_email=EMAIL_HOST_USER,
                  recipient_list=[s.user.email])
