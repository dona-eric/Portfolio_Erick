from django.forms import ModelForm
from .models import Contact, Service, Skill, ServiceRequest, Newsletter
from django import forms

class ContactForms(forms.ModelForm):
    class Meta:
        model = Contact
        fields= ['name', "email", "message"]
    widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre nom complet'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'exemple@email.com'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Votre message...'
            }),
        }
    labels = {
            'name': 'Nom complet',
            'email': 'Adresse email',
            'message': 'Message'
        }

class ServiceForms(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'icon']
    widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du service'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Description du service'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Icone du service'
            }),
        }
    labels = {
            'title': 'Nom du service',
            'description': 'Description',
            'icon': 'Icone'
        }

class ServiceRequestForms(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['nom','email', 'téléphone', 'entreprise', 'details_project', 'budget_estimated', 'delai_livraison']
    widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre nom complet'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email du client'
            }),
            'téléphone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'téléphone du client'
            }),
            'entreprise': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'entreprise du client'
            }),
            'details_project': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'détails du projet'
            }),
            'budget_estimated': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'budget estimé'
            }),
            'delai_livraison': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'delai de livraison'
            }),
        }
    labels = {
            'nom': 'Nom complet',
            'email': 'Adresse email',
            'téléphone': 'Téléphone',
            'entreprise': 'Entreprise',
            'details_project': 'Détails du projet',
            'budget_estimated': 'Budget estimé',
            'delai_livraison': 'Delai de livraison'
        }
                
                
class SkillForms(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['skills_name', 'description']
    widgets = {
            'skills_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la compétence'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Description de la compétence'
            }),
        }
    labels = {
            'skills_name': 'Nom de la compétence',
            'description': 'Description'
        }

class NewsletterForms(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['nom', 'prenom', 'email']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Newsletter.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà inscrit à la newsletter.")
        return email

