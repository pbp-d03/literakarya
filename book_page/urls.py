from django.urls import path, include
from book_page.views import get_books,show_list_books,show_book

app_name = "book_page"

urlpatterns = [
    path('api/', get_books,name="get_books"), # ini buat nampilin api (json buku)
    path('',show_list_books,name="show_list_books"),
    path('book/<int:id>', show_book, name = "show_book")
]
