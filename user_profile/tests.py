import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from user_profile.models import Profile
from book_page.models import Book

class ProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
    
    def test_profile_view(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_create_profile_view(self):
        response = self.client.get(reverse('create_profile'))
        self.assertEqual(response.status_code, 200)

    def test_cari_buku_view(self):
        response = self.client.get(reverse('cari_buku') + '?search=test')
        self.assertEqual(response.status_code, 200)

    def test_rekomen_view(self):
        response = self.client.get(reverse('rekomen'))
        self.assertEqual(response.status_code, 200)

    def test_cari_buku_result(self):
        book = Book.objects.create(nama_buku='Test Book', description='Test Description')
        response = self.client.get(reverse('cari_buku') + '?search=test')
        self.assertContains(response, 'Test Book')

    def test_rekomen_result(self):
        user_profile = Profile.objects.get(user=self.user)
        user_profile.favorite_genre1 = 'Genre1'
        user_profile.favorite_genre2 = 'Genre2'
        user_profile.favorite_genre3 = 'Genre3'
        user_profile.save()

        book = Book.objects.create(nama_buku='Test Book', description='Test Description', genre_1='Genre1')
        response = self.client.get(reverse('rekomen'))
        self.assertContains(response, 'Test Book')

    def test_profile_form_valid(self):
        data = {'field1': 'value1', 'field2': 'value2'}  # Replace with valid form data
        response = self.client.post(reverse('profile'), data)
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content)
        self.assertTrue(json_data['success'])

    def test_profile_form_invalid(self):
        data = {}  # Replace with invalid form data
        response = self.client.post(reverse('profile'), data)
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content)
        self.assertFalse(json_data['success'])
