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

# Configuration
username = os.getenv("USER_ID")
github_username = os.getenv('USERNAME')
github_token = os.getenv('GITHUB_TOKEN')

def make_github_request(url, headers=None):
    """Fonction utilitaire pour faire des requêtes GitHub"""
    if headers is None:
        headers = {'Authorization': f'token {github_token}'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            raise Exception("Token GitHub invalide ou expiré. Veuillez vérifier votre token dans le fichier .env")
        elif response.status_code == 403:
            raise Exception("Limite d'API GitHub atteinte. Veuillez réessayer plus tard")
        else:
            raise Exception(f"Erreur lors de la requête GitHub: {str(e)}")
    except Exception as e:
        raise Exception(f"Erreur lors de la connexion à GitHub: {str(e)}")

def fetch_medium_articles(username):
    """Récupère les articles Medium de l'utilisateur"""
    url = f'https://medium.com/@{username}/latest'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Erreur : Impossible d'accéder au profil Medium (code {response.status_code})")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article')
    
    for article in articles:
        title_element = article.find('h2')
        title = title_element.text.strip() if title_element else "Titre non trouvé"

        link_element = article.find('a', href=True)
        url_blog = 'https://medium.com' + link_element['href'] if link_element else None

        date_element = article.find('time')
        date_published = make_aware(datetime.strptime(date_element['datetime'], '%Y-%m-%dT%H:%M:%S.%fZ')) if date_element else None

        content_element = article.find('p')
        content = content_element.text.strip() if content_element else "Contenu non trouvé"

        tags = [tag.text for tag in article.find_all('a', class_='pw-tag')]

        Article.objects.update_or_create(
            title=title,
            defaults={
                'content': content,
                'url_blog': url_blog,
                'date_published': date_published,
                'categorie': ', '.join(tags) if tags else None,
            }
        )


def get_github_statistics(username, token):
    """Récupère et calcule les statistiques GitHub détaillées en temps réel"""
    # Vérifier le format du token
    if not token.startswith(('ghp_', 'github_pat_')):
        raise Exception("Format de token GitHub invalide. Le token doit commencer par 'ghp_' ou 'github_pat_'")
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Récupérer tous les dépôts
    repos = []
    repos_url = f'https://api.github.com/users/{username}/repos'
    while repos_url:
        response = make_github_request(repos_url, headers)
        repos.extend(response.json())
        repos_url = response.links.get('next', {}).get('url')

    # Statistiques de base
    total_repos = len(repos)
    total_stars = sum(repo['stargazers_count'] for repo in repos)
    total_forks = sum(repo['forks_count'] for repo in repos)
    
    # Langages utilisés
    languages = {}
    for repo in repos:
        if repo['language']:
            languages[repo['language']] = languages.get(repo['language'], 0) + 1
    
    # Récupérer les contributions
    contributions = {
        'yearly': {},
        'daily': {},
        'hourly': {}
    }
    
    # Récupérer les événements de l'utilisateur
    recent_activities = []
    events_url = f'https://api.github.com/users/{username}/events'
    while events_url and len(recent_activities) < 10:  # Limiter à 10 activités récentes
        response = make_github_request(events_url, headers)
        events = response.json()
        
        for event in events:
            if len(recent_activities) >= 10:
                break
                
            event_date = date_parse(event['created_at'])
            
            # Contributions par année
            year = event_date.year
            contributions['yearly'][year] = contributions['yearly'].get(year, 0) + 1
            
            # Contributions par jour
            day = event_date.strftime('%Y-%m-%d')
            contributions['daily'][day] = contributions['daily'].get(day, 0) + 1
            
            # Contributions par heure
            hour = event_date.strftime('%H:00')
            contributions['hourly'][hour] = contributions['hourly'].get(hour, 0) + 1
            
            recent_activities.append({
                'type': event['type'],
                'created_at': event['created_at'],
                'repo': {'name': event['repo']['name']},
                'payload': {'action': event.get('payload', {}).get('action', '')}
            })
        
        events_url = response.links.get('next', {}).get('url')

    # Commits par dépôt
    commits_by_repo = {}
    total_commits = 0
    for repo in repos:
        commits_url = f"https://api.github.com/repos/{username}/{repo['name']}/commits"
        try:
            response = make_github_request(commits_url, headers)
            commits = response.json()
            commits_count = len(commits)
            commits_by_repo[repo['name']] = commits_count
            total_commits += commits_count
        except:
            commits_by_repo[repo['name']] = 0

    # Calculer les pourcentages des langages
    total_lang = sum(languages.values())
    top_languages = {lang: round((count/total_lang)*100, 1) for lang, count in languages.items()}
    top_languages = dict(sorted(top_languages.items(), key=lambda x: x[1], reverse=True)[:5])

    return {
        'total_repos': total_repos,
        'total_stars': total_stars,
        'total_forks': total_forks,
        'total_commits': total_commits,
        'languages': languages,
        'top_languages': top_languages,
        'contributions': contributions,
        'repositories': [{
            'name': repo['name'],
            'description': repo['description'],
            'stargazers_count': repo['stargazers_count'],
            'forks_count': repo['forks_count'],
            'language': repo['language'],
            'html_url': repo['html_url'],
            'updated_at': repo['updated_at'],
            'commits': commits_by_repo.get(repo['name'], 0)
        } for repo in repos],
        'recent_activities': recent_activities
    }

# Appeler la fonction pour récupérer les articles Medium
if username:
    fetch_medium_articles(username)

# github_api.py
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
    """Map les types d'événements GitHub vers des noms plus lisibles"""
    mapping = {
        'PushEvent': 'Push',
        'PullRequestEvent': 'PullRequest',
        'IssuesEvent': 'Issue',
        'CreateEvent': 'Create'
    }
    return mapping.get(event_type)