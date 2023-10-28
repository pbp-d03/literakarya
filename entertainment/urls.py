from django.urls import path
from entertainment.views import (
    entertainment, add_recommendation_ajax, edit_recommendation, 
    delete_recommendation_ajax, like_recommendation
)

app_name = 'entertainment'

urlpatterns = [
    # URL for the main entertainment page
    path('', entertainment, name='entertainment'),

    # URLs for CRUD operations on recommendations
    path('add_recommendation_ajax/', add_recommendation_ajax, name='add_recommendation_ajax'),
    path('edit_recommendation/<int:recommendation_id>/', edit_recommendation, name='edit_recommendation'),
    path('delete_recommendation_ajax/<int:recommendation_id>/', delete_recommendation_ajax, name='delete_recommendation_ajax'),

    # URL for "like" functionality on recommendations
    path('like_recommendation/', like_recommendation, name='like_recommendation'),
]
