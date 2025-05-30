from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404, HttpResponse
from .models import About, Article, Project, Skill, Contact, Service, ServiceRequest, Newsletter, GitHubRepo, GitHubActivity
from .forms import ContactForms, ServiceRequestForms, NewsletterForms, ServiceForms
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt 
import warnings,requests, json, os, traceback
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.db.models import Q,Model
from django.utils.decorators import method_decorator, sync_and_async_middleware, sync_only_middleware
from django.db import models
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, DetailView, ListView
from django.http import JsonResponse
from .utils import get_github_statistics, fetch_medium_articles
from asgiref.sync import sync_to_async
import openai, json, httpx
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

# message d'alerte
warnings.filterwarnings("ignore", message="StreamingHttpResponse must consume synchronous iterators")

#login_required
"""Construction des vues génériques pour les pages de l'application
basée sur les classes de Django"""  

# Page d'accueil
class HomeView(TemplateView):
    template_name = 'portfolio/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_projects'] = Project.objects.all()[:3]  # Affiche les 3 derniers projets
        context['latest_articles'] = Article.objects.all().order_by('-date_published')[:3]  # Affiche les 3 derniers articles
        return context


# Page "À propos de moi"

class AboutView(DetailView):
    model = About
    template_name = 'portfolio/about.html'
    def get_object(self):
        return About.objects.first()


# vues pour les blogs ou articles et les details des blogs
@method_decorator(sync_only_middleware, name='dispatch')
class ArticleListView(ListView):
    model = Article
    template_name = 'portfolio/blog.html'
    context_object_name = 'articles'
    paginate_by = 5  # Affiche 5 articles par page
    ordering = ['-date_published']  # Tri par date de publication
    queryset = Article.objects.all().order_by('-date_published')




## pour les details sur les articles ou blogs
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'portfolio/blog_detail.html'
    context_object_name = 'articles'
    queryset = Article.objects.all()
    

# Page des compétences
class SkillsListView(ListView):
    model = Skill
    template_name = 'portfolio/skills.html'
    context_object_name = 'skills'
    queryset = Skill.objects.all()

# vue des projects
class ProjectListView(ListView):
    model = Project
    template_name = 'portfolio/projects.html'
    context_object_name = 'projects'
    paginate_by = 5  # Affiche 5 projets par page
    queryset = Project.objects.all().prefetch_related('skills_used')  # Si tu as des relations
    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-date_project_update')
        search_query = self.request.GET.get('q')  # Récupère le mot-clé
        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
        return queryset

    
    
# Page des contacts

def send_email_via_mailtrap(subject, body, recipient_email):
    url = "https://sandbox.api.mailtrap.io/api/send/3448761"  # l'api de maitrip pour recevoir des mail des contacts et des newsletters

    headers = {
        "Authorization": f"Bearer {settings.MAILTRAP_API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "from": {
            "email": settings.EMAIL_ADMIN,
            "name": "DataWorld"
        },
        "to": [
            {
                "email": recipient_email
            }
        ],
        "subject": subject,
        "text": body
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("✅ Email envoyé avec succès via Mailtrap API")
        return True
    else:
        print("❌ Échec de l'envoi :", response.status_code, response.text)
        return False


## vue pour les contacts en utilisant les formulaires de django et les vues generiques

def contacts(request):
    if request.method == "POST":
        print("✔ Django a reçu une requête POST !")  # Debugging
        form = ContactForms(request.POST)
        
        if form.is_valid():
            print("✔ Formulaire valide !")  # Debugging
            try:
                nom = form.cleaned_data["name"]
                email = form.cleaned_data["email"]
                message = form.cleaned_data["message"]
                print(f"✔ Formulaire validé : {nom}, {email}, {message}")

                # Construction des messages
                message_admin = f"Message de {nom}, ({email}):\n\n{message}"
                message_user = f"Bonjour {nom},\n\nMerci de nous avoir contactés. Nous avons bien reçu votre message et vous répondrons sous peu.\n\nCordialement,\nL'équipe."

                # Envoi des emails
                mail_admin = send_email_via_mailtrap(
                    subject = f"📩 Nouveau message de : {email}",
                    body = message_admin,
                    recipient_email = settings.EMAIL_ADMIN
                )
                mail_user = send_email_via_mailtrap(
                    subject = "📩 Votre message a bien été reçu !",
                    body = message_user,
                    recipient_email = email
                )

                if mail_admin and mail_user:
                    print("✅ Emails envoyés avec succès !")
                    messages.success(request, "Votre message a été envoyé avec succès ! Nous vous répondrons bientôt.")
                else:
                    print("❌ Erreur lors de l'envoi des emails.")
                    messages.error(request, "Problème lors de l'envoi des emails. Veuillez réessayer.")

                return redirect("home")  # Redirection après succès
            except Exception as e:
                print("❌ Erreur lors de l'envoi de l'email :", e)
                print(traceback.format_exc())  # Debugging avancé
                messages.error(request, "Une erreur est survenue lors de l'envoi de votre message. Veuillez réessayer.")
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = ContactForms()

    return render(request, "portfolio/contacts.html", {"form": form})


# vues pour les services

class ServicesListView(ListView):
    model = Service
    template_name = 'portfolio/services.html'
    context_object_name = 'services'
    paginate_by = 6  # Affiche 6 services par page
    queryset = Service.objects.all().order_by('-created_at')
    
    
##### detail des services
class ServiceDetailView(DetailView):
    model = Service
    template_name = 'portfolio/service_detail.html'
    context_object_name = 'services_detail'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ServiceRequestForms(initial={'service': self.object})
        return context

class ServiceRequestView(FormView):
    form_class = ServiceRequestForms
    template_name = 'portfolio/services_request.html'
    
    def form_valid(self, form):
        service_request = form.save(commit=False)
        service_request.service = get_object_or_404(Service, pk=self.kwargs['pk'])
        service_request.save()
        messages.success(self.request, "Votre demande a été envoyée !")
        return redirect(reverse_lazy('display/services'))  # Redirection vers la page du service

    def form_invalid(self, form):
        messages.error(self.request, "Veuillez corriger les erreurs dans le formulaire.")
        return super().form_invalid(form)





"""vue pour les newsletters """

MAILTRAP_API_TOKEN = os.getenv("MAILTRAP_API_TOKEN")

def send_email_via_mailtrap(nom, prenom, email):
    url = "https://sandbox.api.mailtrap.io/api/send/3448761"

    headers = {
        "Authorization": f"Bearer {MAILTRAP_API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "from": {"email": settings.EMAIL_ADMIN, "name": "DataWorld"},
        "to": [{"email": email}],  # Email Admin
        "subject": "Nouvelle inscription à la newsletter",
        "text": f"Nom: {nom}\nPrénom: {prenom}\nEmail: {email}"
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.status_code == 200


def newsletters(request):
    if request.method == 'POST':
        print("✔ Django a reçu une requête POST !")  # Debugging
        form = NewsletterForms(request.POST)
        if form.is_valid():
            print("✔ Formulaire valide !")  # Debugging
            try:
                nom = form.cleaned_data['nom']
                prenom = form.cleaned_data['prenom']
                email = form.cleaned_data['email']
                print(f"✔ Formulaire validé : {nom}, {prenom}, {email}")

                # Vérifie si l'email existe déjà
                news, created = Newsletter.objects.get_or_create(
                    email=email,
                    defaults={'nom': nom, 'prenom': prenom}
                )

                if created:
                    print("✔ Nouvel inscrit :", news)
                    messages.success(request, f"Merci {nom} ! Vous êtes inscrit à la newsletter")

                    # Envoi d'un email avec Mailtrap API
                    mail_sent = send_email_via_mailtrap(nom, prenom, email)
                    if mail_sent:
                        print("✅ Email envoyé avec succès !")
                    else:
                        print("❌ Erreur lors de l'envoi de l'email.")

                else:
                    print("⚠ Email déjà inscrit :", email)
                    messages.info(request, "Cette adresse est déjà inscrite à notre newsletter")

                return redirect('home')

            except Exception as e:
                print("🚨 Erreur lors de l'inscription :", e)
                messages.error(request, "Une erreur est survenue. Veuillez réessayer.")

    else:
        form = NewsletterForms()

    return render(request, 'portfolio/newsletters.html', {
        'form': form,
        'title': 'Inscription à la newsletter',
        "description": "Restez informé de nos dernières actualités"
    })

"""def newsletters(request):
    if request.method == 'POST':
        form = NewsletterForms(request.POST)
        if form.is_valid():
            try:
                nom = form.cleaned_data['nom']
                prenom = form.cleaned_data['prenom']
                email = form.cleaned_data['email']
                validate_email(email)

                # Vérifie si l'email existe déjà ou crée un nouvel abonné
                news, created = Newsletter.objects.get_or_create(
                    email=email,
                    defaults={'nom': nom, 'prenom': prenom}
                )

                if created:
                    messages.success(request, f"Merci {nom} ! Vous êtes inscrit à la newsletter")
                    print("Nouvelle inscription :", news)

                    # Envoi d'un email à l'administrateur
                    send_mail(
                        'Nouvelle inscription à la newsletter',
                        f'Nom: {nom}\nPrénom: {prenom}\nEmail: {email}',
                        settings.DEFAULT_FROM_EMAIL,
                        [settings.EMAIL_ADMIN],  # Remplace par l'email de l'administrateur
                        fail_silently=False,
                    )
                else:
                    messages.info(request, "Cette adresse est déjà inscrite à notre newsletter")
                
                return redirect('home')  # Redirige vers la page d'accueil
            except ValidationError:
                messages.error(request, "Veuillez fournir une adresse email valide.")
            except Exception as e:
                print("Erreur lors de l'inscription :", e)
                messages.error(request, "Une erreur est survenue. Veuillez réessayer.")
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = NewsletterForms()

    return render(request, 'portfolio/newsletters.html', {
        'form': form,
        'title': 'Inscription à la newsletter',
        "description": "Restez informé de nos dernières actualités"
    })

"""
            

""" Une fonction qui valide tout les formulaires de la base avec get ou post"""

#class FormValidationMixin:

    ## mixin pour la validation des formulaires avec gestion des messages
    #def form_valid(self, form):
     #   try:
      #      self.object = form.save()
       #     messages.success(self.request, self.get_success_message())
        #    return HttpResponseRedirect(self.get_success_url())
        #except Exception as e:
         #   messages.error(
          #      self.request,
           #     f"Une erreur est survenue: {str(e)}"
            #)
            #return self.form_invalid(form)
        

    #def form_invalid(self, form):
     #   messages.error(
      #      self.request,
       #     "Veuillez corriger les erreurs dans le formulaire"
        #)
        #return super().form_invalid(form)
    
   # def get_success_message(self):
    #    return f"Vos modifications ont été prises en compte !"

    #def get_success_url(self):
     #   return reverse('home')**

## vue pur les repos github
def github_activity(request):
    username = os.getenv('USERNAME')
    token = os.getenv('GITHUB_TOKEN')
    
    # Debug information
    print(f"Username: {username}")
    print(f"Token exists: {bool(token)}")
    print(f"Token length: {len(token) if token else 0}")
    print(f"Token format: {token[:10] if token else 'None'}")
    
    if not username or not token:
        return render(request, 'portfolio/error.html', {
            'error_message': f"Configuration GitHub manquante. Veuillez vérifier les variables d'environnement: {'USERNAME' if not username else ''} {'GITHUB_TOKEN' if not token else ''}"
        })
    
    try:
        stats = get_github_statistics(username, token)
        return render(request, 'portfolio/github.html', {'stats': stats})
    except Exception as e:
        print(f"Error fetching GitHub stats: {str(e)}")
        return render(request, 'portfolio/error.html', {
            'error_message': f"Erreur lors de la récupération des statistiques GitHub: {str(e)}"
        })
        
        
        
"""ASSIISTANT IA AVEC MISTRAL API"""

api_mistral=os.getenv('API_MISTRAL')
@csrf_exempt
def assistant_ai(request):
    if request.method=="POST":
        data = json.loads(request.body)
        user_input = data.get("question", )
        system_prompt = """
    Tu es l'assistant personnel de Eric Koulodji. Réponds aux questions à propos de :
    - Ses projets (Gestion des stocks et de ventes des articles téléphoniques,
    Annotation automatique d'images africaines,  Risque Scoring de crédit bancaire etc.).
    - Son CV (Data Scientist, Développeur Web Django & Machine Learning Specialist).
    - Ses stacks (Django, FastAPI, React, Python, etc.).
    Sois clair, précis et utile.
        """

        headers = {
            "Authorization": f"Bearer {api_mistral}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "mistral-small-latest",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        }

        with httpx.Client(timeout=7) as client:
            response = client.post(
                "https://api.mistral.ai/v1/chat/completions",
                headers=headers,
                json=payload
            )

        answer = response.json()["choices"][0]["message"]["content"]
        return JsonResponse({"answer": answer})
