from django.test import TestCase
from django.urls import reverse
from .models import URL
from django.contrib.auth.models import User

class URLModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.url = URL.objects.create(
            original_url='https://www.example.com',
            short_url='exmpl',
            user=self.user
        )

    def test_url_creation(self):
        self.assertEqual(self.url.original_url, 'https://www.example.com')
        self.assertEqual(self.url.short_url, 'exmpl')
        self.assertEqual(self.url.clicks, 0)
        self.assertIsNotNone(self.url.created_at)

    def test_url_str(self):
        self.assertEqual(str(self.url), 'https://www.example.com -> exmpl')

class URLViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.url = URL.objects.create(
            original_url='https://www.example.com',
            short_url='exmpl',
            user=self.user
        )  # Создание объекта URL с short_url='exmpl'

    def test_redirect_to_original_url(self):
        response = self.client.get(reverse('redirect_to_original', args=['exmpl']))
        self.assertRedirects(response, 'https://www.example.com', fetch_redirect_response=False)

    def test_create_url_view(self):
        response = self.client.post(reverse('create_url'), {
            'original_url': 'https://www.new-url.com',
            'short_url': 'newurl'  # Убедитесь, что это поле присутствует в форме, если оно используется
        })
        self.assertEqual(response.status_code, 302)  # Проверяем, что редирект произошел
        self.assertTrue(URL.objects.filter(original_url='https://www.new-url.com').exists())  # Проверяем, что URL создан

class UserRegistrationTest(TestCase):
    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'Str0ngP@ssw0rd!',
            'password2': 'Str0ngP@ssw0rd!'
        })
        # Вывод ошибок формы, если статус не 302
        if response.status_code != 302:
            print(response.context['form'].errors)

        self.assertEqual(response.status_code, 302)  # Проверяем, что редирект произошел
        self.assertTrue(User.objects.filter(username='newuser').exists())

class UserDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_user_detail_view(self):
        response = self.client.get(reverse('user_detail', args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')