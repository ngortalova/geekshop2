import json
import os

from authapp.models import ShopUser, ShopUserProfile
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "create user profiles"

    def handle(self, *args, **options):
        users = ShopUser.objects.all()
        for user in users:
            ShopUserProfile.objects.create(user=user)



