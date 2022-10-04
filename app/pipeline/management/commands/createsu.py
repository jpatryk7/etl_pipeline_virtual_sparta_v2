from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import environ
import os


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(username='superuser').exists():
            User.objects.create_superuser('superuser', 'su@su.none', 'su-pass')
