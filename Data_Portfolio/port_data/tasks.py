from celery import shared_task
from .utils import fetch_github_data, fetch_medium_articles


@shared_task
def fetch_github_data_task(username, token):
    """
    Celery task to fetch GitHub data for a given username.
    """
    return fetch_github_data(username, token)


def fetch_medium_articles_task(username):
    """
    Celery task to fetch Medium articles for a given username.
    """
    return fetch_medium_articles(username)
    