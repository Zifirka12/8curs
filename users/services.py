import stripe
from config.settings import API_KEY
from datetime import datetime, timedelta
import json
from django_celery_beat.models import PeriodicTask, IntervalSchedule

stripe.api_key = API_KEY


def create_stripe_product(payment):
    return stripe.Product.create(name=f"{payment.course if payment.course else payment.lesson}")


def create_price(amount, product):
    return stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product=product.get("id")
    )


def create_stripe_session(price):
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")


def ban_unactive_users():
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=2,
        period=IntervalSchedule.DAYS,
    )
    PeriodicTask.objects.create(
        interval=schedule,
        name='Ban unactive users',
        task='users.tasks.check_last_login',
        kwargs=json.dumps({
            'be_careful': True,
        }),
        expires=datetime.now() + timedelta(seconds=30)
    )
