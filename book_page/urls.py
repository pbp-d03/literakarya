from django.urls import path, include
from book_page.views import get_books

app_name = "book_page"

urlpatterns = [
    path('api/', get_books,name="get_books"), # ini buat nampilin api (json buku)
]
