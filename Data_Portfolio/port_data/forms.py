from django.forms import ModelForm
from .models import Contact, Service, Skill, ServiceRequest, Newsletter
from django import forms

class ContactForms(forms.ModelForm):
    class Meta:
        model = Contact
        fields= ['name', "email", "subject", "message"]
    widgets = {
        'name' :forms.TextInput(attrs={"class": "form-control"}),
        'email' : forms.EmailInput(attrs={'class': "form-control"}),
        "subject": forms.TextInput(attrs={'class':"form-control"}),
        'message' : forms.TextInput(attrs={"class": "form-control"})
    }


class ServiceRequestForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    service = forms.ModelChoiceField(queryset=Service.objects.all())
    message = forms.CharField(widget=forms.Textarea)


class NewsletterForms(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['nom', 'prenom', 'email']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Newsletter.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà inscrit à la newsletter.")
        return email

