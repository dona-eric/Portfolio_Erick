# management/commands/update_github.py
from django.core.management.base import BaseCommand
from .github_api import fetch_github_data

class Command(BaseCommand):
    help = 'Update GitHub data'

    def handle(self, *args, **options):
        fetch_github_data(
            username='dona-eric',
            token='votre_token_github'
        )
        self.stdout.write('GitHub data updated successfully!')
