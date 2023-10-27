from django.urls import path, include
from book_page.views import get_books,show_list_books,show_book,get_komen_json,add_comment_ajax

app_name = "book_page"

urlpatterns = [
    path('api/', get_books,name="get_books"), # ini buat nampilin api (json buku)
    path('',show_list_books,name="show_list_books"),
    path('book/<int:id>', show_book, name = "show_book"),

    path('add-komen/<int:id1>', add_comment_ajax, name = "add_komen_ajax"),
    path('get-komen/<int:id1>', get_komen_json, name='get_komen_json')
]
