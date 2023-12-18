from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.core import serializers
from ereading.forms import EreadingForm
from ereading.models import Ereading
from book_page.models import Book
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json

@login_required(login_url='/login')
def show_dashboard(request):
    books = Book.objects.all()
    genres = list_genres(books)
    dict_books = json.dumps(book_genres_dict(books))
    form = EreadingForm(request.POST or None)

    if request.user.username == "adminliterakarya":
        context = {
            'name' : request.user.username,
            'genres' : genres,
            'dict_books' : dict_books,
            'ereadings' : Ereading.objects.all(),
            'form' : form
        }
        return render(request, "admin_dashboard.html", context)
    
    else:
        context = {
            'name' : request.user.username,
            'genres' : genres,
            'dict_books' : dict_books,
            'ereadings' : Ereading.objects.filter(user=request.user),
            'form' : form
        }
        return render(request, "dashboard.html", context)

# Membuat list berisi daftar genre.
def list_genres(books):
    unique_genres = set()

    for book in books:
        for i in range(1, 6):
            genre_key = f'genre_{i}'
            genre_value = getattr(book, genre_key, None)
            if genre_value:
                unique_genres.add(genre_value)

    return sorted(unique_genres)

# Membuat dictionary dengan key buku dan value semua genrenya.
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
        ereadings = Ereading.objects.all() # Jika user adalah admin.
    
    else:
        ereadings = Ereading.objects.filter(user=request.user) # Jika user bukan admin.

    return HttpResponse(serializers.serialize('json', ereadings), content_type="application/json")

@csrf_exempt
def add_ereading(request):
    formdata = json.loads(request.body)
    form = EreadingForm(formdata or None)

    if form.is_valid() and request.method == "POST":
        ereading = form.save(commit=False)
        ereading.user = request.user
        ereading.save()
        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

@csrf_exempt
def delete_ereading(request):
    if request.method=="POST":
        id = request.POST.get("id")
        ereading = Ereading.objects.get(pk=id)
        ereading.delete()
        return HttpResponse(status=201)
    
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
        return HttpResponse(status=201)
    
    return HttpResponseNotFound()

# Proyek Akhir Semester
@csrf_exempt
def get_json_user(request, uname):
    global ereading, filteruser
    if uname == "adminliterakarya":
        ereading = Ereading.objects.all()
        return HttpResponse(serializers.serialize("json", ereading), content_type="application/json")

    else:
        ereadings = Ereading.objects.all()
        for e in ereadings:
            if e.user.username == uname:
                filteruser = e.user
                break
        
        ereading = Ereading.objects.filter(user = filteruser)
        return HttpResponse(serializers.serialize("json", ereading), content_type="application/json")

@csrf_exempt
def add_ereading_flutter(request):
    if request.method == "POST":
        formdata = json.loads(request.body)
        form = EreadingForm(formdata or None)
        ereading = form.save(commit=False)
        ereading.user = request.user
        ereading.save()
        return JsonResponse({"status": "success"}, status=200)
    
    else:
        return JsonResponse({"status": "error"}, status=401)