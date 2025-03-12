import requests, os
from bs4 import BeautifulSoup
from datetime import datetime
from django.utils.timezone import make_aware
from .models import Article
from dotenv import load_dotenv
import requests
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

def fetch_github_data(username, token):
    headers = {'Authorization': f'token {token}'}
    
    # Récupération des repos
    repos_url = f'https://api.github.com/users/{username}/repos'
    repos = requests.get(repos_url, headers=headers).json()
    
    for repo in repos:
        repo_obj, created = GitHubRepo.objects.update_or_create(
            name=repo['name'],
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
        
        # Récupération des activités
        events_url = f"https://api.github.com/repos/{username}/{repo['name']}/events"
        events = requests.get(events_url, headers=headers).json()
        
        for event in events:
            activity_type = _map_event_type(event['type'])
            if activity_type:
                GitHubActivity.objects.update_or_create(
                    id=event['id'],
                    defaults={
                        'repo': repo_obj,
                        'activity_type': activity_type,
                        'message': event['payload'].get('commits', [{}])[0].get('message', '') if activity_type == 'Push' else event['type'],
                        'timestamp': datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ'),
                        'url': event['repo']['url']
                    }
                )

def _map_event_type(event_type):
    mapping = {
        'PushEvent': 'Push',
        'PullRequestEvent': 'PullRequest',
        'IssuesEvent': 'Issue',
        'CreateEvent': 'Create'
    }
    return mapping.get(event_type)
