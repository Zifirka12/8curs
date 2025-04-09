from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from materials.models import Course, Lesson


# from django.forms import URLField


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True,
        verbose_name="Почта",
    )
    phone = models.CharField(
        max_length=11,
        verbose_name="Телефон",
        null=True,
        blank=True,
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Аватарка",
        help_text="Вставьте аватарку",
        null=True,
        blank=True,
    )
    city = models.CharField(
        max_length=50,
        verbose_name="Город",
        help_text="Введите город проживания",
        null=True,
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    PAYMENT_STATUS = [
        ("cash", "наличные"),
        ("transfer", "перевод на счет"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user',
        verbose_name="Юсер"
    )
    payment_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Data оплаты"
    )
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='course',
        verbose_name="Оплаченный курсик",
        null=True, blank=True
    )
    separately_paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='lesson',
        verbose_name="Оплаченный зум",
        null=True,
        blank=True
    )
    payment_amount = models.IntegerField(
        default=0,
        verbose_name="Сумма оплаты",
        null=True,
        blank=True
    )
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS,
        default="cash",
        verbose_name="варианты оплаты",
        null=True,
        blank=True
    )
    link = models.URLField(
        verbose_name="ссылка на оплаты",
        max_length=400,
        blank=True,
        null=True)
    session_id = models.CharField(
        "ID сессии",
        max_length=255,
        blank=True,
        null=True)

    def __str__(self):
        return f'{self.user} {self.paid_course}'

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"

    def __str__(self):
        return self.session_id
