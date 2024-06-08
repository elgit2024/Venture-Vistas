from django.core.management.base import BaseCommand
from django.utils import timezone
from blog.models import Tour

class Command(BaseCommand):
    help = 'Deletes MessMenu objects where day is in the past'

    def handle(self, *args, **kwargs):
        menudeleted = Tour.objects.filter(expiry__lt=timezone.now())
        for m in menudeleted:
            m.delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleaned up MessMenu objects'))

