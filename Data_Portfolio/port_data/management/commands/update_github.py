# management/commands/update_github.py
from django.core.management.base import BaseCommand
from port_data.utils import fetch_github_data, fetch_medium_articles
from .sync_medium import Command as SyncMediumCommand
import os
from dotenv import load_dotenv

load_dotenv()

class Command(BaseCommand):
    help = 'Update GitHub data'

    def handle(self, *args, **options):
        fetch_github_data(
            username=os.getenv('GITHUB_USERNAME'),
            token=os.getenv('GITHUB_TOKEN')
        )
        self.stdout.write('GitHub data updated successfully!')
