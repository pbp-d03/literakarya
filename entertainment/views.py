from django.shortcuts import render, redirect
from .models import Book, Review
from .forms import ReviewForm

def review_book(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = Review(user=request.user, book=form.cleaned_data['book'], rating=form.cleaned_data['rating'], review=form.cleaned_data['review'])
            review.save()
            request.user.points += 10
            request.user.save()
            return redirect('entertainment_space')
    else:
        form = ReviewForm()
    return render(request, 'review_book.html', {'form': form})
