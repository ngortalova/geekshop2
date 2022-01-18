from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
import pytz
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


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


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'
    SMN_ELSE = 'S'

    GENDER_CHOICES = (
        (MALE, 'Мужчина'),
        (FEMALE, 'Женщина'),
        (SMN_ELSE, 'Небинарный?')
    )

    user = models.OneToOneField(ShopUser, unique=True, null=False,\
                                db_index=True, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='теги', max_length=128, \
                               blank=True)
    aboutMe = models.TextField(verbose_name='о себе', max_length=512, \
                               blank=True)
    gender = models.CharField(verbose_name='пол', max_length=1, \
                              choices=GENDER_CHOICES, blank=True)

    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=ShopUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.shopuserprofile.save()
