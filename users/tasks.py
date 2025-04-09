from users.models import User
from datetime import timedelta
from django.utils import timezone


def check_last_login():
    users = User.objects.all()

    for user in users:
        if timezone.now() - user.last_login > timedelta(days=30):
            user.is_active = False
        user.save()
