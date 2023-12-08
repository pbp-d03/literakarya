from django.urls import path, include
from book_page.views import get_books,show_list_books,show_book,get_komen_json,add_comment_ajax,\
                            show_bookmark,add_bookmark_ajax,delete_bookmark,add_likes,delete_komen,show_filtered_flutter

app_name = "book_page"

urlpatterns = [
    path('api/', get_books,name="get_books"), # ini buat nampilin api (json buku)
    path('',show_list_books,name="show_list_books"),
    path('book/<int:id>/', show_book, name = "show_book"),

    path('bookmark/', show_bookmark, name = "show_bookmark"),

    path('add-komen/<int:id1>/', add_comment_ajax, name = "add_comment_ajax"),
    path('get-komen/<int:id1>/', get_komen_json, name='get_komen_json'),

    path('add-bookmark/<int:id>/', add_bookmark_ajax, name = "add_bookmark_ajax"),
    path('delete-bookmark/<int:id>/', delete_bookmark, name = "delete_bookmark"),

    path('add-likes/<int:id>/', add_likes, name = "add_likes"),
    path('delete-komen/<int:id>/', delete_komen, name = "delete_komen"),

    path('book-filter/<str:hasil_cari>/', show_filtered_flutter, name = "show_filtered_flutter"),
]
