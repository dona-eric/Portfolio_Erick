import requests, os
from bs4 import BeautifulSoup
from datetime import datetime
from django.utils.timezone import make_aware
from .models import Article
from dotenv import load_dotenv
import requests
from django.db import transaction
from dateutil.parser import parse as date_parse

from django.utils import timezone
from datetime import datetime
from .models import GitHubRepo, GitHubActivity
load_dotenv()

# Récupérer le nom d'utilisateur Medium depuis les variables d'environnement
username = os.getenv("USER_ID")
def fetch_medium_articles(username):
    # URL de votre profil Medium
    url = f'https://medium.com/@{username}/latest'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Faire une requête HTTP pour récupérer le contenu de la page
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Erreur : Impossible d'accéder au profil Medium (code {response.status_code})")
        return

    # Parser le HTML avec BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Trouver tous les articles
    articles = soup.find_all('article')
    for article in articles:
        # Extraire le titre
        title_element = article.find('h2')
        title = title_element.text.strip() if title_element else "Titre non trouvé"

        # Extraire le lien de l'article
        link_element = article.find('a', href=True)
        url_blog = 'https://medium.com' + link_element['href'] if link_element else None

        # Extraire l'auteur (vous, dans ce cas)
        author_articles = username

        # Extraire la date de publication
        date_element = article.find('time')
        date_published = make_aware(datetime.strptime(date_element['datetime'], '%Y-%m-%dT%H:%M:%S.%fZ')) if date_element else None

        # Extraire le contenu (résumé)
        content_element = article.find('p')
        content = content_element.text.strip() if content_element else "Contenu non trouvé"

        # Extraire les catégories (tags)
        tags = [tag.text for tag in article.find_all('a', class_='pw-tag')]

        # Enregistrer l'article dans la base de données
        Article.objects.update_or_create(
            title=title,
            defaults={
                'content': content,
                'url_blog': url_blog,
                'author_articles': author_articles,
                'date_published': date_published,
                'categorie': ', '.join(tags) if tags else None,
            }
        )

# Appeler la fonction pour récupérer les articles
fetch_medium_articles(username=username)


# github_api.py
username = os.getenv('USERNAME')
def fetch_github_data(username, token):
    headers = {'Authorization': f'token {token}'}
    
    # Fetch all pages for repositories
    repos = []
    repos_url = f'https://api.github.com/users/{username}/repos'
    while repos_url:
        response = requests.get(repos_url, headers=headers)
        response.raise_for_status()  # Check for HTTP errors
        repos.extend(response.json())
        repos_url = response.links.get('next', {}).get('url')  # Pagination

    with transaction.atomic():
        for repo in repos:
            # Use repo owner from API data
            owner_login = repo['owner']['login']
            repo_name = repo['name']
            
            repo_obj, _ = GitHubRepo.objects.update_or_create(
                name=repo_name,
                defaults={
                'description': repo['description'],
                'html_url': repo['html_url'],
                'stars': repo['stargazers_count'],
                'forks': repo['forks_count'],
                'language': repo['language'],
                'created_at': datetime.strptime(repo['created_at'], '%Y-%m-%dT%H:%M:%SZ'),
                'updated_at': datetime.strptime(repo['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
            }
        )
            
            # Fetch all pages for events
            events = []
            events_url = f"https://api.github.com/repos/{owner_login}/{repo_name}/events"
            while events_url:
                response = requests.get(events_url, headers=headers)
                response.raise_for_status()
                events.extend(response.json())
                events_url = response.links.get('next', {}).get('url')

            activities = []
            for event in events:
                activity_type = _map_event_type(event['type'])
                if not activity_type:
                    continue
                
                # Safely get commit message
                commits = event.get('payload', {}).get('commits') or [{}]
                message = commits[0].get('message', '') if commits else ''
                
                activities.append(GitHubActivity(
                    id=event['id'],
                    repo=repo_obj,
                    activity_type=activity_type,
                    message=message[:255],  # Truncate to 255 chars
                    timestamp=date_parse(event['created_at']),
                    url=event.get('repo', {}).get('url', '')
                ))
            
            # Bulk create/update activities
            GitHubActivity.objects.bulk_create(
                activities,
                update_conflicts=True,
                update_fields=['message', 'timestamp', 'url'],
                unique_fields=['id']
            )
            
def _map_event_type(event_type):
    mapping = {
        'PushEvent': 'Push',
        'PullRequestEvent': 'PullRequest',
        'IssuesEvent': 'Issue',
        'CreateEvent': 'Create'
    }
    return mapping.get(event_type)