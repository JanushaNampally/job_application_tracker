from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from applications.models import JobApplication

class Command(BaseCommand):
    help = 'Automatically update job application statuses based on time elapsed'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Number of days after which to mark applications as Rejected if no update',
        )

    def handle(self, *args, **options):
        days = options['days']
        cutoff_date = timezone.now() - timedelta(days=days)

        # Update applications that haven't been updated in the last 'days' days and are still 'Applied'
        updated_count = JobApplication.objects.filter(
            status='Applied',
            last_updated__lt=cutoff_date
        ).update(status='Rejected')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated {updated_count} job applications to "Rejected" status.'
            )
        )
