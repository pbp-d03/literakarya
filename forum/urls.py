from django.urls import path, include
from forum.views import create_post_flutter, create_reply_flutter, delete_post_flutter, show_forum, add_post, add_reply, delete_post, delete_reply, get_posts_json, get_replies_json

app_name = "forum"

urlpatterns = [
    path('', show_forum,name="show_forum"),
    path('add-post/', add_post, name='add_post'),
    path('add-reply/<int:id>', add_reply, name='add_reply'),
    path('delete-post/<int:id>', delete_post, name='delete_post'),
    path('delete-reply/<int:id>', delete_reply, name='delete_reply'),
    path('json/all-posts/', get_posts_json, name="get_posts"),
    path('json/all-replies/<int:id>', get_replies_json, name="get_replies"),
    path('create-post-flutter/', create_post_flutter, name='create_post_flutter'),
    path('create-reply-flutter/', create_reply_flutter, name='create_reply_flutter'),
    path('delete-post-flutter/', delete_post_flutter, name='delete_post_flutter'),
]
