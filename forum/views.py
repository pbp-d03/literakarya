from django.shortcuts import render
from book_page.models import Book

# Create your views here.
def show_main(request):
    books = Book.objects.all()
    context = {
        'books' : books
    }
    return render(request, "forum.html", context)