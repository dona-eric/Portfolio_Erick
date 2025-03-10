from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .views import (HomeView, AboutView, 
                    ArticleDetailView, ArticleListView,
                    ServicesListView, ServiceDetailView,
                    ServiceRequestView, ProjectListView, SkillsListView)


urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    path('about-me/', AboutView.as_view(), name='about'),
    path('skills/', SkillsListView.as_view(), name='skills'),
    path('projects/', ProjectListView.as_view(), name='projects'),
    path('blog/', ArticleListView.as_view(), name='blog_list'),
    path('blog/<int:pk>/', ArticleDetailView.as_view(), name='blog_detail'),
    path('display/services/', ServicesListView.as_view(), name='display/services'),
    path('display/service/<int:pk>/', ServiceDetailView.as_view(), name='detail/display/services'),
    path('services/<int:pk>/demande/', ServiceRequestView.as_view(), name='services/requested'),
    path('contacts-us/', views.contacts, name='contacts-us'),
    path('news/', views.newsletters, name = 'news'),
    path('github/', views.github_activity, name = 'github'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)