from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404, HttpResponse
from .models import About, Article, Project, Skill, Contact, Service, ServiceRequest, Newsletter
from .forms import ContactForms, ServicesForms, ServiceRequestForms, NewsletterForms
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.urls import reverse
from django.views.generic.edit import FormView
from django.conf import settings
import warnings,requests, json, os
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, DetailView
# Page d'accueil

#login_required

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



# Page des articles dew blog

def article(request):
    blog_article = Article.objects.all().order_by('-date_published')
    paginator = Paginator(blog_article, 5)  # Affiche 5 articles par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'portfolio/blog.html', {'page_obj': page_obj})

#pour une article spécifique

def article_list(request, id_article):
    blog_list = get_object_or_404(Article, pk=id_article)
    return render(request, 'portfolio/blog_list.html', {'blog_list': blog_list})


# Page des compétences
def skills(request):
    skill = Skill.objects.all()
    return render(request, 'portfolio/skills.html', {'skills': skill})


# Page des projets
def projects(request):
    project = Project.objects.all().prefetch_related('skills_used')  # Si tu as des relations
    return render(request, 'portfolio/projects.html', {'project': project})



# Page des contacts

def contacts(request):
    if request.method == "POST":
        print("✔ Django a reçu une requête POST !")  # Debugging
        form = ContactForms(request.POST)
        if form.is_valid():
            print("✔ Formulaire valide !")  # Debugging
            try:
                nom = form.cleaned_data["name"]
                email = form.cleaned_data["email"]
                subject_message = form.cleaned_data["subject"]
                content_message = form.cleaned_data["message"]
                print(f"✔ Formulaire validé : {nom}, {email}, {content_message}")

                # Email à l'admin
                full_message = f"Message de {nom} ({email}):\n\n{content_message}"
                print(full_message)
                mail_admin = send_mail(
                    subject=f"📩 Nouveau message de {nom} : {subject_message}",
                    message=full_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.EMAIL_ADMIN],  # Ton email admin
                    fail_silently=False,
                )

                # Email de confirmation à l'utilisateur
                mail_user = send_mail(
                    subject="📩 Votre message a bien été reçu !",
                    message=f"Bonjour {nom},\n\nMerci de nous avoir contactés. Nous avons bien reçu votre message et vous répondrons sous peu.\n\nCordialement,\nL'équipe.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],  # Email du visiteur
                    fail_silently=False,
                )

                if mail_admin and mail_user:
                    print("✅ Emails envoyés avec succès !")
                    messages.success(request, "Votre message a été envoyé avec succès ! Nous vous répondrons bientôt.")
                else:
                    print("❌ Erreur lors de l'envoi des emails.")

                return redirect("home")  # Redirige vers la page d'accueil
            except Exception as e:
                print("Erreur lors de l'envoi de l'email :", e)
                messages.error(request, "Une erreur est survenue lors de l'envoi de votre message. Veuillez réessayer.")
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = ContactForms()

    return render(request, "portfolio/contacts.html", {"form": form})

# vues pour les services

def services(request):
    service =  Service.objects.all()
    return render(request, 'portfolio/services.html',
                  {'service_list': service})


def services_detail(request, id_service):
    service_detail = get_object_or_404(Service, pk=id_service)
    return render(request, 'portfolio/service_detail.html', {'service_detail': service_detail})




def services_request(request, id_service=None):
    service = get_object_or_404(Service, pk=id_service) if id_service else None
    
    if request.method == 'POST':
        form = ServiceRequestForms(request.POST)
        if form.is_valid():
            try:
                service_request = form.save(commit=False)
                if service:
                    service_request.service = service
                service_request.save()
                messages.success(request, 'Votre demande de service a été envoyée avec succès!')
                return redirect('services')
            except Exception as e:
                print("Erreur lors de l'enregistrement de la demande de service :", e)
                messages.error(request, "Une erreur est survenue lors de l'enregistrement de votre demande. Veuillez réessayer.")
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = ServiceRequestForms()
        if service:
            form.initial = {'service': service}
    
    contexte = {
        'form': form,
        'service': service,
    }
    return render(request, 'portfolio/services_request.html', contexte)


"""vue pour les newsletters """



MAILTRAP_API_TOKEN = settings.MAILTRAP_API_TOKEN

def send_email_via_mailtrap(nom, prenom, email):
    url = "https://sandbox.api.mailtrap.io/api/send/3448761"

    headers = {
        "Authorization": f"Bearer {MAILTRAP_API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "from": {"email": settings.DEFAULT_FROM_EMAIL, "name": "Mon Site"},
        "to": [{"email": settings.EMAIL_ADMIN}],  # Email Admin
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


#def newsletters(request):
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
     #   return reverse('home')


#warnings.filterwarnings("ignore", message="StreamingHttpResponse must consume synchronous iterators")
