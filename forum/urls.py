from django.urls import path, include
from forum.views import show_forum, add_post, add_reply, delete_post, delete_reply, get_posts_json, get_replies_json

app_name = "book_page"

urlpatterns = [
    path('', show_forum,name="show_forum"),
    path('add-post/', add_post, name='add_post'),
    path('add-reply/<int:id>', add_reply, name='add_reply'),
    path('delete-post/<int:id>', delete_post, name='delete_post'),
    path('delete-reply/<int:id>', delete_reply, name='delete_reply'),
    path('json/all-posts/', get_posts_json, name="get_posts"),
    path('json/all-replies/<int:id>', get_replies_json, name="get_replies"),
]
