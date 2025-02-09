from django.forms import ModelForm
from .models import Contact, Service, Skill, ServiceRequest, Newsletter
from django import forms

class ContactForms(forms.ModelForm):
    class Meta:
        model = Contact
        fields= ['nom', "prenom", "email", "phone", "subject", "message"]
    widgets = {
        'nom' :forms.TextInput(attrs={"class": "form-control"}),
        'prenom': forms.TextInput(attrs={"class": "form-control"}),
        'email' : forms.EmailInput(attrs={'class': "form-control"}),
        'phone':forms.TextInput(attrs={"class": "form-control"}),
        "subject": forms.TextInput(attrs={'class':"form-control"}),
        'message' : forms.TextInput(attrs={"class": "form-control"})
    }


class ServicesForms(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'icon', 'price']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Titre du service', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description du service', 'class': 'form-control'}),
            'icon': forms.TextInput(attrs={'placeholder': 'Icône (ex. fa-solid fa-code)', 'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Prix', 'class': 'form-control'}),
        }
        exclude = ('icon', "price")


class ServiceRequestForms(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['service', 'client', 'message']
        widgets = {
            'client': forms.Select(attrs={"class": "form-control"}),  # Utilisation de Select pour ForeignKey
            'service': forms.Select(attrs={"class": "form-control"}),  # Utilisation correcte
            'message': forms.Textarea(attrs={"class": "form-control", "placeholder": "Votre message", "rows": 4}),
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

