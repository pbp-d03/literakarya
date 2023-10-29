from django.test import TestCase
from django.urls import reverse
from .models import Book, Bookmark, Comment
from .forms import KomenForm
from django.contrib.auth.models import User

class BookPageTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.book = Book.objects.create(nama_buku='Test Book', description='Test description')
        self.comment = Comment.objects.create(user='testuser', buku=self.book, isi_komen='Test comment')

    def test_get_books(self):
        response = self.client.get(reverse('get_books'))
        self.assertEqual(response.status_code, 200)

    def test_show_list_books(self):
        response = self.client.get(reverse('show_list_books'))
        self.assertEqual(response.status_code, 200)

    def test_show_bookmark(self):
        response = self.client.get(reverse('show_bookmark'))
        self.assertEqual(response.status_code, 200)

    def test_add_bookmark_ajax(self):
        response = self.client.post(reverse('add_bookmark_ajax', args=[self.book.id]))
        self.assertEqual(response.status_code, 201)

    def test_show_book(self):
        response = self.client.get(reverse('show_book', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)

    def test_get_komen_json(self):
        response = self.client.get(reverse('get_komen_json', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)

    def test_add_comment_ajax(self):
        response = self.client.post(reverse('add_comment_ajax', args=[self.book.id]), {'isi_komen': 'Test comment'})
        self.assertEqual(response.status_code, 201)

    def test_delete_bookmark(self):
        response = self.client.delete(reverse('delete_bookmark', args=[self.book.id]))
        self.assertEqual(response.status_code, 201)

    def test_add_likes(self):
        response = self.client.post(reverse('add_likes', args=[self.comment.id]))
        self.assertEqual(response.status_code, 201)

    def test_delete_komen(self):
        response = self.client.delete(reverse('delete_komen', args=[self.comment.id]))
        self.assertEqual(response.status_code, 201)

    def test_login_required_views(self):
        response = self.client.get(reverse('show_list_books'))
        self.assertEqual(response.status_code, 302)  # 302 is the status code for a redirect when not logged in
