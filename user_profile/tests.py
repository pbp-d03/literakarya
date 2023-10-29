from django.test import TestCase
from django.test import TestCase, Client
from django.urls import reverse
from user_profile.models import Profile
from django.contrib.auth.models import User 

# Create your tests here.
class profileTest(TestCase):
    def setUp(self):
        # Membuat pengguna untuk pengujian
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.profile = Profile.objects.create(
            user=self.user,
            first_name='akun',
            last_name='pertama',
            bio='aku yang terdepan',
            address='jalan Margonda',
            favorite_genre1='Fiction',
            favorite_genre2='Novels',
            favorite_genre3='Childrens',
        )

    def test_show_profile_view(self):
        # Menggunakan self.client untuk mengakses URL
        user01 = Profile.objects.get(first_name="akun")
        self.assertEqual(user01.user, self.user)
        self.assertEqual(user01.last_name, "pertama")
        self.assertEqual(user01.bio, "aku yang terdepan")
        self.assertEqual(user01.address, "jalan Margonda")
        self.assertEqual(user01.favorite_genre1, "Fiction")
        self.assertEqual(user01.favorite_genre2, "Novels")
        self.assertEqual(user01.favorite_genre3, "Childrens")