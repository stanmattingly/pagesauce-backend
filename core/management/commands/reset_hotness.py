from django.core.management.base import BaseCommand
from app.models import Content


class Command(BaseCommand):

    def handle(self, *args, **options):
        for content in Content.objects.all():
            content.reset_hotness()
            content.save()

        

