from django.contrib import admin

from .models import Project, Skill, Newsletter, Article, Contact, About, ServiceRequest, Service
# Register your models here.


class ProjectAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Élements Important', {"fields": ["title", "description", "skills_used", 'image_project']}),
        ('Information utiles', {"fields":["github_link", "url_project"]}),
        ]

admin.site.register(Project, ProjectAdmin)

admin.site.register(About)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    
admin.site.register(Service, ServiceAdmin)

class ServiceRequestdmin(admin.ModelAdmin):
    list_display = ("nom","email", "téléphone", "entreprise", "details_project", "budget_estimated", "delai_livraison", "date_requested")
    list_filter =("service", "nom", 'email', 'entreprise')
    search_fields = ("service", 'nom')

admin.site.register(ServiceRequest, ServiceRequestdmin)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_article', 'date_published', 'categorie', 'content', 'url_blog', "image_article")
    list_filter = ('author_article', 'categorie', 'date_published')
    search_fields = ('title', 'content', 'author_article')
    date_hierarchy = 'date_published'
    ordering = ('-date_published',)
admin.site.register(Article, ArticleAdmin)


class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'subscribed_at', 'is_active')
    list_filter = ('subscribed_at', "is_active")
    search_fields = ('email', 'nom', "prenom")
admin.site.register(Newsletter, NewsletterAdmin)


class SkillAdmin(admin.ModelAdmin):
    list_display = ('category', 'skills_name',)
    search_fields = ('category', "description")
admin.site.register(Skill, SkillAdmin)



class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','email', 'message', 'sent_at', 'is_read')
    list_filter = ('is_read', 'sent_at')
    search_fields = ('name','email','message')

admin.site.register(Contact, ContactAdmin)