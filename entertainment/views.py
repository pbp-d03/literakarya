from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.core import serializers
from django.db.models import Q
from entertainment.models import Recommendation
from entertainment.forms import BookRecommendationForm
from book_page.models import Book
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib import messages

@login_required
def entertainment(request):
    form = None
    recommendations = Recommendation.objects.all().order_by('-date')
    books = Book.objects.all()

    # Mengambil semua genre yang unik dari setiap field genre
    genre_1_list = Book.objects.values_list('genre_1', flat=True).distinct()
    genre_2_list = Book.objects.values_list('genre_2', flat=True).distinct()
    genre_3_list = Book.objects.values_list('genre_3', flat=True).distinct()
    genre_4_list = Book.objects.values_list('genre_4', flat=True).distinct()
    genre_5_list = Book.objects.values_list('genre_5', flat=True).distinct()

    # Menggabungkan semua daftar genre dan mengambil set yang unik
    all_genres = set(genre_1_list) | set(genre_2_list) | set(genre_3_list) | set(genre_4_list) | set(genre_5_list)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
        selected_genre = request.POST.get('selected_genre', None)
        if selected_genre:
            filtered_books = books.filter(
                Q(genre_1=selected_genre) | 
                Q(genre_2=selected_genre) |
                Q(genre_3=selected_genre) |
                Q(genre_4=selected_genre) |
                Q(genre_5=selected_genre)
            )
        else:
            filtered_books = books

        topic_options = [{'value': book.nama_buku, 'text': book.nama_buku} for book in filtered_books]
        return JsonResponse({'topic_options': topic_options})

    context = {
    'user': request.user.username,
    'book_choices': books,
    'all_genres': all_genres,
    'recommendations': recommendations,  
    }

    return render(request, 'entertainment.html', context)

@csrf_exempt
@login_required
def add_recommendation_ajax(request):
    if request.method == 'POST':
        form = BookRecommendationForm(request.POST)
        if form.is_valid():
            new_recommendation = form.save(commit=False)
            new_recommendation.user = request.user
            new_recommendation.save()
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "form_invalid"})

@login_required
def edit_recommendation(request, recommendation_id):
    recommendation = get_object_or_404(Recommendation, id=recommendation_id)
    if request.user == recommendation.user:
        if request.method == 'POST':
            form = BookRecommendationForm(request.POST, instance=recommendation)
            if form.is_valid():
                form.save()
                return JsonResponse({"status": "edited"})
        else:
            form = BookRecommendationForm(instance=recommendation)
        context = {'form': form, 'recommendation': recommendation}
        return render(request, 'edit_recommendation.html', context)
    else:
        return JsonResponse({"status": "unauthorized"})

@csrf_exempt
@login_required
def delete_recommendation_ajax(request, recommendation_id):
    recommendation = get_object_or_404(Recommendation, id=recommendation_id)
    if request.user == recommendation.user:
        recommendation.delete()
        return JsonResponse({"status": "deleted"})
    else:
        return JsonResponse({"status": "unauthorized"})

@csrf_exempt
@login_required
def like_recommendation(request):
    if request.method == 'POST':
        recommendation_id = request.POST.get('recommendation_id')
        recommendation = get_object_or_404(Recommendation, id=recommendation_id)
        user = request.user
        if user in recommendation.likes.all():
            recommendation.likes.remove(user)
            liked = False
        else:
            recommendation.likes.add(user)
            liked = True
        like_count = recommendation.likes.count()
        return JsonResponse({'liked': liked, 'like_count': like_count})
