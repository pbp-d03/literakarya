from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from entertainment.models import Recommendation
from entertainment.forms import BookRecommendationForm
from book_page.models import Book
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

@login_required
def entertainment(request):
    # Initialize the form variable as None
    form = None

    # Mengambil semua rekomendasi untuk ditampilkan dalam carousel
    recommendations = Recommendation.objects.all().order_by('-date')
    books = Book.objects.all()

    # Inisialisasi form rekomendasi buku
    if request.method == 'POST':
        form = BookRecommendationForm(request.POST)
        if form.is_valid():
            new_recommendation = form.save(commit=False)
            new_recommendation.user = request.user
            new_recommendation.save()
            return redirect('entertainment')  # Replace with the appropriate URL
    else:
        form = BookRecommendationForm()

    # Make sure form is not None before reaching this point
    if form is None:
        form = BookRecommendationForm()

    context = {
        'form': form,
        'user': request.user.username,
        'recommendations': recommendations,
        'book_choices': books,
    }
    
    return render(request, 'entertainment/forms.html', context)

@login_required
def edit_recommendation(request, recommendation_id):
    recommendation = get_object_or_404(Recommendation, id=recommendation_id)

    if request.user == recommendation.user:
        if request.method == 'POST':
            form = BookRecommendationForm(request.POST, instance=recommendation)
            if form.is_valid():
                form.save()
                return redirect('entertainment')  # Ganti dengan URL yang sesuai
        else:
            form = BookRecommendationForm(instance=recommendation)

        context = {'form': form, 'recommendation': recommendation}
        return render(request, 'entertainment/edit_recommendation.html', context)
    else:
        messages.error(request, 'Anda tidak memiliki izin untuk mengedit rekomendasi ini.')
        return redirect('entertainment')

@login_required
def delete_recommendation(request, recommendation_id):
    recommendation = get_object_or_404(Recommendation, id=recommendation_id)

    if request.user == recommendation.user:
        recommendation.delete()
        return redirect('entertainment')  # Ganti dengan URL yang sesuai
    else:
        messages.error(request, 'Anda tidak memiliki izin untuk menghapus rekomendasi ini.')
        return redirect('entertainment')

# Tambahkan dekorator csrf_exempt hanya jika benar-benar diperlukan
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
