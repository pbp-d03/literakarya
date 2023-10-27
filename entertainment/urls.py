from django.urls import path
from entertainment.views import entertainment, edit_recommendation, delete_recommendation, like_recommendation

app_name = 'entertainment'

urlpatterns = [
    # URL untuk halaman utama entertainment
    path('', entertainment, name='entertainment'),

    # URL untuk mengedit rekomendasi buku
    path('edit/<int:recommendation_id>/', edit_recommendation, name='edit_recommendation'),

    # URL untuk menghapus rekomendasi buku
    path('delete/<int:recommendation_id>/', delete_recommendation, name='delete_recommendation'),

    # URL untuk "like" pada rekomendasi buku
    path('like/<int:recommendation_id>/', like_recommendation, name='like_recommendation'),
]
