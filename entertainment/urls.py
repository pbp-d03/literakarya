from django.urls import path
from . import views

urlpatterns = [
    path('review/', views.review_book, name='review_book'),
]
