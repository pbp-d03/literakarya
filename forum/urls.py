from django.urls import path, include
from forum.views import show_forum

app_name = "book_page"

urlpatterns = [
    path('', show_forum,name="show_forum"),
]
