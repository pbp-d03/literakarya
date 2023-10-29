from django.urls import path
from recommendation.views import show_recommendation, membuat_rekomendasi, show_json, show_json_by_id, get_books_by_genre, edit_rekom, hapus_rekom, like_view

app_name = 'recommendation'

urlpatterns = [
    path('', show_recommendation, name='show_recommendation'),
    path('bikin/', membuat_rekomendasi, name='bikin'),
    path('json/', show_json, name='show_json'), 
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'), 
    path('get_books_by_genre/<str:genre>/', get_books_by_genre, name='get_books_by_genre'),
    path('edit-rekom/<int:id>', edit_rekom, name='edit_rekom'),
    path('hapus-rekom/<int:id>', hapus_rekom, name='hapus_rekom'), 
    path('like/<int:pk>/', like_view, name='like_view'),
]