from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
import pytz
from django.conf import settings


class ShopUser(AbstractUser):
    city = models.CharField(max_length=64, verbose_name="город", blank=True)
    phone_number = models.CharField(max_length=14, verbose_name="телефон", blank=True)
    avatar = models.ImageField(upload_to="user_avatars", blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст', default=18, blank=True, null=True)
    is_active = models.BooleanField(verbose_name="живой", default=True)
    activation_key = models.CharField(max_length=128, verbose_name="ключ активации", blank=True, null=True)
    activation_key_expires = models.DateTimeField(blank=True, null=True)

    def is_activation_key_expired(self):
        if datetime.now(pytz.timezone(settings.TIME_ZONE)) <= self.activation_key_expires + timedelta(hours=48):
            return False
        return True

    def activate_user(self):
        self.is_active = True
        self.activation_key = None
        self.activation_key_expires = None
        self.save()
