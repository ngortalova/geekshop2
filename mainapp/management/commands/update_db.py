from authapp.models import ShopUser, ShopUserProfile
from django.core.management.base import BaseCommand
from mainapp.utils import get_or_create


class Command(BaseCommand):
    help = "create user profiles"

    def handle(self, *args, **options):
        users = ShopUser.objects.all()
        for user in users:
            get_or_create(ShopUserProfile, user=user)
