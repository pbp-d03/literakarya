import json
import logging
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
from django.views.decorators.http import require_POST

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

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Rekomendasi, Book

@csrf_exempt
def membuat_rekomendasi_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Validasi data
            genre_buku = data['genre_buku']
            judul_buku = data['judul_buku']
            nilai_buku = data['nilai_buku']
            isi_rekomendasi = data['isi_rekomendasi']

            # Buat objek Rekomendasi
            rekomendasi = Rekomendasi(
                genre_buku=genre_buku,
                judul_buku=Book.objects.get(pk=judul_buku),  # asumsi nama_buku adalah field di model Book
                nilai_buku=float(nilai_buku),
                isi_rekomendasi=isi_rekomendasi,
                user=request.user
            )
            rekomendasi.save()

            return JsonResponse({'status': 'success', 'message': 'Rekomendasi berhasil dibuat'}, status=200)

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

def like_view(request, pk):
    post = get_object_or_404(Rekomendasi, id=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    post.save()
    return HttpResponseRedirect(reverse('recommendation:show_recommendation'))  

@csrf_exempt
@require_POST
def like_unlike_flutter(request, pk):
    
    try:
        data = json.loads(request.body)
        user_id = data['user_id']
        action = data['action']

        user = get_object_or_404(User, username=user_id)
        rekomendasi = get_object_or_404(Rekomendasi, pk=pk)

        if action == 'like':
            rekomendasi.likes.add(user)
        elif action == 'unlike':
            rekomendasi.likes.remove(user)

        total_likes = rekomendasi.likes.count()
        is_liked = user in rekomendasi.likes.all()

        return JsonResponse({
            'status': 'success',
            'message': 'Action performed successfully',
            'total_likes': total_likes,
            'is_liked': is_liked,
        }, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
    except Rekomendasi.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Recommendation not found'}, status=404)
    except Exception as e:
        logging.error(f"Error in like_unlike_flutter: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
def edit_rekom_flutter(request, id):
    rekomendasi = get_object_or_404(Rekomendasi, pk=id)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rekomendasi = get_object_or_404(Rekomendasi, pk=id)

            # Update fields if provided
            rekomendasi.genre_buku = data['genre_buku']
            rekomendasi.judul_buku = Book.objects.get(pk=data['judul_buku'])
            rekomendasi.nilai_buku = float(data['nilai_buku'])
            rekomendasi.isi_rekomendasi = data['isi_rekomendasi']

            rekomendasi.save()

            return JsonResponse({'status': 'success', 'message': 'Rekomendasi berhasil diperbarui'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def hapus_rekom_flutter(request, rekomendasi_id):
    rekomendasi = get_object_or_404(Rekomendasi, pk=rekomendasi_id)

    if request.method == 'DELETE':
        try:
            rekomendasi = get_object_or_404(Rekomendasi, pk=rekomendasi_id)
            rekomendasi.delete()

            return JsonResponse({'status': 'success', 'message': 'Rekomendasi berhasil dihapus'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
