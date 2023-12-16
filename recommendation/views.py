from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from recommendation.forms import FormRekomendasi
from recommendation.models import Rekomendasi
from django.urls import reverse
from django.http import HttpResponse
from book_page.models import Book
from django.core import serializers
from django.http import JsonResponse 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@login_required(login_url='/login')
def show_recommendation(request):
    recommended = Rekomendasi.objects.all().select_related('user')
    pk = request.GET.get('pk', None)
    if pk is not None:
        total = get_object_or_404(Rekomendasi, id=pk)
        total_likes = total.total_likes()
    else:
        total_likes = 0  # or any other default value

    context = {
        'user': request.user.username,
        'recommended' : recommended,
        'total_likes' : total_likes,
    }

    return render(request, "recommendation.html", context)

@csrf_exempt
@login_required(login_url='/login/')  # Make sure the user is logged in
def membuat_rekomendasi(request):
    form = FormRekomendasi(request.POST or None)
    books_by_genre = {}
    all_books = Book.objects.all()

    for book in all_books:
        genre = book.genre_1
        if genre not in books_by_genre:
            books_by_genre[genre] = []
        books_by_genre[genre].append(book.id)

    if form.is_valid() and request.method == "POST":
        instance = form.save(commit=False)
        if instance.nilai_buku < 0 or instance.nilai_buku > 5:
            context = {
                'form': form, 
                'error_message': "Rating harus antara 0 dan 5", 
                'books_by_genre': books_by_genre
            }
            return render(request, "bikin.html", context)
        instance.user = request.user
        instance.save()
        return HttpResponseRedirect(reverse('recommendation:show_recommendation'))

    context = {'form': form, 'books_by_genre': books_by_genre}
    return render(request, "bikin.html", context)

@csrf_exempt
@login_required(login_url='/login/')  # Pastikan pengguna telah terautentikasi
def membuat_rekomendasi_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = FormRekomendasi(data)
            
            if form.is_valid():
                rekomendasi = form.save(commit=False)
                rekomendasi.user = request.user  # Gunakan pengguna yang terautentikasi
                rekomendasi.save()
                return JsonResponse({'status': 'success', 'message': 'Rekomendasi berhasil dibuat'}, status=200)
            else:
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def show_json(request):
    data = Rekomendasi.objects.all()
    response = []

    for rekomendasi in data:
        book_title = rekomendasi.judul_buku.nama_buku  # Access the book title
        response.append({
            'model': 'recommendation.rekomendasi',
            'pk': rekomendasi.pk,
            'fields': {
                'user': rekomendasi.user.id,
                'gambar_buku': rekomendasi.get_book_image(),  # Get the book image URL/path
                'genre_buku': rekomendasi.genre_buku,
                'judul_buku': book_title,  # Include the book title here
                'nilai_buku': str(rekomendasi.nilai_buku),
                'isi_rekomendasi': rekomendasi.isi_rekomendasi,
                'tanggal': rekomendasi.tanggal.isoformat(),
                'likes': list(rekomendasi.likes.values_list('id', flat=True)),
            }
        })

    return JsonResponse(response, safe=False)  # Return the manually built response as JSON


def show_json_by_id(request, id):
    data = Rekomendasi.objects.filter(pk=id)
    response = []

    for rekomendasi in data:
        book_title = rekomendasi.judul_buku.nama_buku  # Access the book title
        response.append({
            'model': 'recommendation.rekomendasi',
            'pk': rekomendasi.pk,
            'fields': {
                'user': rekomendasi.user.id,
                'gambar_buku': rekomendasi.get_book_image(),  # Get the book image URL/path
                'genre_buku': rekomendasi.genre_buku,
                'judul_buku': book_title,  # Include the book title here
                'nilai_buku': str(rekomendasi.nilai_buku),
                'isi_rekomendasi': rekomendasi.isi_rekomendasi,
                'tanggal': rekomendasi.tanggal.isoformat(),
                'likes': list(rekomendasi.likes.values_list('id', flat=True)),
            }
        })

    return JsonResponse(response, safe=False)  # Return the manually built response as JSON

def get_genres(request):
    genres = Book.objects.values_list('genre_1', flat=True).distinct()
    return JsonResponse(list(genres), safe=False)

def get_books_by_genre(request, genre):
    books = Book.objects.filter(genre_1=genre).values('id', 'nama_buku')
    book_list = list(books)
    return JsonResponse(book_list, safe=False)

def edit_rekom(request, id):
    recommended = Rekomendasi.objects.get(pk = id)
    form = FormRekomendasi(request.POST or None, instance=recommended)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('recommendation:show_recommendation'))

    context = {'form': form}
    return render(request, "edit_rekom.html", context)

def hapus_rekom(request, id):
    recommended = Rekomendasi.objects.get(pk = id)
    recommended.delete()
    return HttpResponseRedirect(reverse('recommendation:show_recommendation'))

@login_required(login_url='/login/')
def like_view(request, pk):
    post = get_object_or_404(Rekomendasi, id=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    post.save()
    return HttpResponseRedirect(reverse('recommendation:show_recommendation'))  
