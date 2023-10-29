from django.test import TestCase
from django.contrib.auth.models import User
from recommendation.models import Rekomendasi
from book_page.models import Book

class RekomendasiTestCase(TestCase):
    
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.book1 = Book.objects.create(nama_buku='Book1', genre_1='Genre1') # tambahkan field lain sesuai dengan model Book Anda
        self.rekomendasi1 = Rekomendasi.objects.create(
            user=self.user1, 
            genre_buku='Genre1', 
            judul_buku=self.book1, 
            nilai_buku=4.5, 
            isi_rekomendasi='This is a recommendation'
        )
        
    def test_rating_validation(self):
        with self.assertRaises(Exception):  # Harapkan sebuah exception
            Rekomendasi.objects.create(
                user=self.user1, 
                genre_buku='Genre1', 
                judul_buku=self.book1, 
                nilai_buku=6.0,  # Rating tidak valid
                isi_rekomendasi='This is another recommendation'
            )
