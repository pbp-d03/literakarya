from django.test import TestCase, Client
from django.contrib.auth.models import User
from ereading.models import Ereading
import json

class DashboardViewTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user('adminliterakarya', '', 'adminpassword')
        self.normal_user = User.objects.create_user('testuser', '', 'testpassword')

    def test_show_dashboard_admin(self):
        self.client.login(username='adminliterakarya', password='adminpassword')
        response = self.client.get('/ereading/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_dashboard.html')

    def test_show_dashboard_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/ereading/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')

class EreadingUserTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_add_ereading_valid_data(self):
        data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'description': 'Test Description',
            'link': 'http://example.com/'
        }
        response = self.client.post('/ereading/add-ereading/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Ereading.objects.count(), 1)

    def test_add_ereading_invalid_data(self):
        data = {
            'title': '', # Invalid data
            'author': 'Test Author',
            'description': 'Test Description',
            'link': 'http://example.com/'
        }
        response = self.client.post('/ereading/add-ereading/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Ereading.objects.count(), 0)

    def test_delete_ereading(self):
        ereading = Ereading.objects.create(
            title='Test Book',
            author='Test Author',
            description='Test Description',
            link='http://example.com/',
            user=self.user
        )
        response = self.client.post('/ereading/delete-ereading/', {'id': ereading.id})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Ereading.objects.count(), 0)

class EreadingAdminTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(username='adminliterakarya', password='adminpassword')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.ereading = Ereading.objects.create(
            title='Test Book',
            author='Test Author',
            description='Test Description',
            link='http://example.com/',
            user=self.user
        )

    def test_accept_ereading(self):
        self.client.login(username='adminliterakarya', password='adminpassword')
        response = self.client.post('/ereading/accept-ereading/', {'id': self.ereading.id})
        self.assertEqual(response.status_code, 201)
        self.ereading.refresh_from_db()
        self.assertEqual(self.ereading.state, 1)
        self.assertIsNotNone(self.ereading.last_updated)

    def test_reject_ereading(self):
        self.client.login(username='adminliterakarya', password='adminpassword')
        response = self.client.post('/ereading/reject-ereading/', {'id': self.ereading.id})
        self.assertEqual(response.status_code, 201)
        self.ereading.refresh_from_db()
        self.assertEqual(self.ereading.state, 2)
        self.assertIsNotNone(self.ereading.last_updated)