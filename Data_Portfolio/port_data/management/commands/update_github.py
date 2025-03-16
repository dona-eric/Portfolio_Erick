# management/commands/update_github.py
from django.core.management.base import BaseCommand
from port_data.utils import fetch_github_data, fetch_medium_articles
from .

class Command(BaseCommand):
    help = 'Update GitHub data'

    def handle(self, *args, **options):
        fetch_github_data(
            username='dona-eric',
            token="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"
        )
        self.stdout.write('GitHub data updated successfully!')
