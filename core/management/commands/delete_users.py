from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):
        for user in User.objects.exclude(username="stanmattingly").exclude(username="spmattingly1@gmail.com"):
            print(user.username)
            user.delete()