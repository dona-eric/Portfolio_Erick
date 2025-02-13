from django.core.management.base import BaseCommand
from port_data.models import Article
from port_data.utils import fetch_medium_articles

import os
from dotenv import load_dotenv

load_dotenv()  # Charger les variables d'environnement

class Command(BaseCommand):
    help = "Synchroniser les articles Medium avec la base de données"

    def handle(self, *args, **kwargs):
        # Récupérer le nom d'utilisateur Medium depuis l'environnement
        USER_ID = os.getenv('USER_ID')

        if not USER_ID:
            self.stdout.write(self.style.ERROR("La variable d'environnement USER_ID est introuvable. Vérifiez votre fichier .env."))
            return

        self.stdout.write(f"Récupération des articles pour l'utilisateur Medium : {USER_ID}")
        
        # Récupérer les articles via la fonction utilitaire
        try:
            articles = fetch_medium_articles(USER_ID)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erreur lors de la récupération des articles : {e}"))
            return

        if not articles:
            self.stdout.write(self.style.WARNING("Aucun article récupéré ! Vérifiez l'API ou l'utilisateur Medium."))
            return

        # Parcourir les articles récupérés et les synchroniser
        for article_data in articles:
            try:
                article, created = Article.objects.update_or_create(
                    title=article_data.get('title', 'Titre indisponible'),
                    defaults={
                        'content': article_data.get('content', ''),
                        'date_published': article_data.get('date_published', None),
                        'categorie': ", ".join(article_data.get('categorie', [])),  # Transformer en chaîne si c'est une liste
                        'author_articles': article_data.get('author', ''),
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Nouvel article créé : {article_data.get('title', 'Sans titre')}"))
                else:
                    self.stdout.write(self.style.SUCCESS(f"Article mis à jour : {article_data.get('title', 'Sans titre')}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Erreur lors de la synchronisation de l'article '{article_data.get('title', 'Sans titre')}' : {e}"))

        self.stdout.write(self.style.SUCCESS("Tous les articles ont été synchronisés avec succès !"))
