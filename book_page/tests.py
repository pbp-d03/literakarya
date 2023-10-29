from django.test import TestCase, Client
from django.contrib.auth.models import User
from ereading.models import Ereading
import json

class TampilanBukuTest(TestCase):
    def setUp(self):
        self.normal_user = User.objects.create_user('testuser', '', 'testpassword')

    def test_show_list_books(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tampilan_buku.html')

    def test_show_book(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/books/book/1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'info_buku.html')

    def test_show_bookmark(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/books/bookmark')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookmark.html')

