from django.test import TestCase, Client
from django.urls import reverse
from .models import Article, Service, Newsletter

class ArticleViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.article = Article.objects.create(
            title="Test Article",
            content="This is a test article.",
            author_articles="Test Author",
            date_published="2023-10-01"
        )

    def test_article_list_view(self):
        response = self.client.get(reverse('article_list', args=[self.article.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Article")

    def test_article_detail_view(self):
        response = self.client.get(reverse('article_detail', args=[self.article.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Article")

class ServicesViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.service = Service.objects.create(
            title="Test Service",
            description="This is a test service.",
            price=100
        )

    def test_services_detail_view(self):
        response = self.client.get(reverse('services_detail', args=[self.service.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Service")

class NewsletterViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_newsletter_subscription(self):
        response = self.client.post(reverse('newsletters'), {
            'nom': 'Test',
            'prenom': 'User',
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 302)  # Redirection après succès
        self.assertTrue(Newsletter.objects.filter(email='test@example.com').exists())