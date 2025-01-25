import requests
from datetime import datetime

def recuperer_articles_medium(USER_ID):
    # URL de l'API Medium (via RSS-to-JSON)
    url = f"https://api.rss2json.com/v1/api.json?rss_url=https://medium.com/feed/@{USER_ID}"
    try:
        response = requests.get(url, timeout=10)  # Timeout pour éviter les blocages
        response.raise_for_status()  # Lève une exception pour les erreurs HTTP
        data = response.json()

        # Récupérer les articles
        articles = data.get('items', [])  # Utilisation de 'items' au lieu de 'item'
        if not articles:
            print("Aucun article trouvé dans la réponse.")
            return []

        # Traiter chaque article
        return [
            {
                'title': article.get('title', 'Titre non disponible'),
                'content': article.get('content', 'Contenu non disponible'),
                'categorie': article.get('categories', []),  # Peut être une liste
                'date_published': datetime.strptime(article['pubDate'], "%a, %d %b %Y %H:%M:%S %Z") if 'pubDate' in article else None,
                'author': article.get('author', 'Auteur inconnu')
            }
            for article in articles
        ]
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête à l'API Medium : {e}")
    except ValueError as ve:
        print(f"Erreur lors de l'analyse des données : {ve}")
    except Exception as ex:
        print(f"Erreur inattendue : {ex}")
    return []
