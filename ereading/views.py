from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound, JsonResponse
from django.core import serializers
from ereading.models import Ereading
from book_page.models import Book
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json

@login_required(login_url='/login')
def show_dashboard(request):
    books = Book.objects.all()
    genres = list_genres(books)
    dict_books = json.dumps(book_genres_dict(books))

    if request.user.username == "adminliterakarya":
        context = {
            'name' : request.user.username,
            'genres' : genres,
            'dict_books' : dict_books,
            'ereadings' : Ereading.objects.all(),
        }
        return render(request, "admin_dashboard.html", context)
    
    else:
        context = {
            'name' : request.user.username,
            'genres' : genres,
            'dict_books' : dict_books,
            'ereadings' : Ereading.objects.filter(user=request.user)
        }
        return render(request, "dashboard.html", context)

def list_genres(books):
    unique_genres = set()

    for book in books:
        for i in range(1, 6):
            genre_key = f'genre_{i}'
            genre_value = getattr(book, genre_key, None)
            if genre_value:
                unique_genres.add(genre_value)

    return sorted(unique_genres)

def book_genres_dict(books):
    book_genres_dict = {}

    for book in books:
        book_genres = []

        for i in range(1, 6):
            genre_key = f'genre_{i}'
            genre_value = getattr(book, genre_key, None)
            if genre_value:
                book_genres.append(genre_value)

        book_genres_dict[book.nama_buku] = book_genres

    return book_genres_dict

def get_json(request):
    if request.user.username == "adminliterakarya":
        ereadings = Ereading.objects.all()
    
    else:
        ereadings = Ereading.objects.filter(user=request.user)

    return HttpResponse(serializers.serialize('json', ereadings))

def show_json(request):
    data = Ereading.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
def add_ereading(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        description = request.POST.get("description")
        link = request.POST.get("link")
        user = request.user

        ereading = Ereading(title=title, author=author, description=description, link=link, user=user)
        ereading.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

@csrf_exempt
def delete_ereading(request):
    if request.method=="POST":
        id = request.POST.get("id")
        ereading = Ereading.objects.get(pk=id)
        ereading.delete()
        return HttpResponse(b"DELETED", status=201)
    
    return HttpResponseNotFound()

@csrf_exempt
def accept_ereading(request):
    if request.method=="POST":
        id = request.POST.get("id")
        ereading = Ereading.objects.get(pk=id)
        ereading.state = 1
        ereading.last_updated = timezone.now()
        ereading.save(update_fields=["state", "last_updated"])
        return HttpResponse(status=201)
    
    return HttpResponseNotFound()

@csrf_exempt
def reject_ereading(request):
    if request.method=="POST":
        id = request.POST.get("id")
        ereading = Ereading.objects.get(pk=id)
        ereading.state = 2
        ereading.last_updated = timezone.now()
        ereading.save(update_fields=["state", "last_updated"])
        return HttpResponse(b"DELETED", status=201)
    
    return HttpResponseNotFound()