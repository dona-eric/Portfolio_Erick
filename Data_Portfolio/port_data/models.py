from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

""" Here we create other that the models of database of website
portfolio """

"""Models  for About"""


class About(models.Model):
    nom = models.CharField(max_length=100)
    prenoms = models.CharField(max_length=150)
    biography = models.TextField(verbose_name="Biographie", help_text="Brève description de vous")
    profil_pictures = models.ImageField(upload_to='portfolio/', blank=True, null=True)
    resume_link = models.URLField(blank=True, null=True)
    #social_media = models.ManyToManyField('social_media.SocialMedia', blank=True)

    class Meta:
        verbose_name = "À propos"
        verbose_name_plural = "À propos"

    def __str__(self):
        return f"{self.nom} {self.prenoms}"
    
    
"""models for skills"""

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('DATA', 'Data Science'),
        ('Python', 'Django-Flasks'),
        ('Mlops', 'Mlop Data Infra'),
        ('DATABASE', 'SQL, MySQL, PostgreSQL'),
        ('DEEP lEARNING', 'Tensorflow, Keras, Pytorch'),
        ("NLP:Natural Language Processing", 'NLTK, Spacy, Gensim, word2vec'),
        ('MACHINE lEARNING', 'Scikit-learn, XGBoost, LightGBM'),
    ]
    category = models.CharField(max_length=200, choices=CATEGORY_CHOICES, default="Category", verbose_name="Catégorie")
    skills_name = models.CharField(max_length=100, verbose_name="Nom de la compétence")
    level = models.IntegerField(
        default=50,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Niveau de maîtrise",
        help_text="Niveau de maîtrise en pourcentage (0-100)"
    )
    description = models.TextField(null=True, blank=True, verbose_name="Description")

    def __str__(self):
        return f"{self.skills_name} ({self.category})"    
    

"""models for projects"""

class Project(models.Model):
    title = models.CharField(max_length=500, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    skills_used = models.ManyToManyField(Skill, related_name="projects", verbose_name="Compétences utilisées")
    image_project = models.ImageField(upload_to='media/', blank=True, null=True, verbose_name="Image du projet")
    github_link = models.URLField(blank=True, null=True, verbose_name="Lien GitHub")
    url_project = models.URLField(blank=True, null=True, verbose_name="URL du projet")
    date_project_update = models.DateTimeField(auto_now_add=True, verbose_name="Date de mise à jour")

    def has_github_link(self):
        return bool(self.github_link)

    def has_demo_link(self):
        return bool(self.url_project)

    def __str__(self):
        return f"{self.title} ({self.description})"
    class Meta:
        ordering = ['-date_project_update']  # Ordre décroissant par date de création
        indexes = [
            models.Index(fields=['-date_project_update']),  # Optionnel : améliore les performances
        ]



"""models for articles """

class Article(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    url_blog = models.URLField(blank=True, null=True)
    author_article= models.CharField(max_length=200, verbose_name='Auteur', null=True)
    date_published = models.DateTimeField(null=True, verbose_name='Date de publication')
    categorie = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title



"""models for contacts: i would like to use the forms of django 
to create it """

class Contact(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nom")
    email = models.EmailField(verbose_name="Adresse email")
    message = models.TextField(verbose_name="Message")
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name="Envoyé à")
    is_read = models.BooleanField(default=False, verbose_name="Lu")

    def __str__(self):
        return f"Message de {self.nom} ({self.email})"
    
    
# mes services 
class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(
        max_length=50,
        default='fa-code',
        blank=False)
    created_at = models.DateTimeField(auto_now= True, verbose_name= 'date de création')
    updated_at = models.DateTimeField(auto_now=True, verbose_name= 'date update')

    def __str__(self):
        return self.title

## models pour permettre à un client de demander des services

class ServiceRequest(models.Model):
    service = models.ForeignKey("Service", on_delete=models.CASCADE, related_name='requests')
    client = models.ForeignKey("Contact", on_delete=models.CASCADE, related_name='service_requests')
    message = models.TextField(verbose_name="Message")
    date_requested = models.DateTimeField(auto_now_add=True, verbose_name="Date de la demande")

    def __str__(self):
        return f"Demande de service de {self.client.name} pour {self.service.title}"



## models pour la newsletter 


class Newsletter(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=200, verbose_name="Prénom")
    email = models.EmailField(unique=True, verbose_name="Adresse email")
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")
    is_active = models.BooleanField(default=True, verbose_name="Actif")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Abonné à la newsletter"
        verbose_name_plural = "Abonnés à la newsletter"
  
# models pour le repo GitHub 

class GitHubRepo(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    url = models.URLField()
    stars = models.IntegerField()
    forks = models.IntegerField()
    language = models.CharField(max_length=50, blank=True)
    last_updated = models.DateTimeField()

    class Meta:
        verbose_name = "Dépôt GitHub"
        verbose_name_plural = "Dépôts GitHub"

    def __str__(self):
        return self.name

class GitHubActivity(models.Model):
    ACTIVITY_TYPES = [
        ('Push', 'Push'),
        ('PullRequest', 'Pull Request'),
        ('Issue', 'Issue'),
        ('Create', 'Create'),
    ]
    
    repo = models.ForeignKey(GitHubRepo, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    message = models.TextField()
    timestamp = models.DateTimeField()
    url = models.URLField()

    class Meta:
        verbose_name = "Activité GitHub"
        verbose_name_plural = "Activités GitHub"
        ordering = ['-timestamp']
        
        def __str__(self):
            return f"{self.repo.name} - {self.activity_type}"