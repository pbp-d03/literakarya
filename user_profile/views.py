from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from user_profile.forms import ProfileForm
from user_profile.models import Profile
from book_page.models import Book
from django.db.models import Q

@login_required
def profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {'form': form})

@login_required
def create_profile(request):
    if not hasattr(request.user, 'profile'):
        user_profile = Profile(user=request.user)
        user_profile.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Profile already exists'})

def cari_buku(request):
    # Ambil kata kunci pencarian dari request GET
    keyword = request.GET.get('search', '')

    # Cari buku yang sesuai dengan kata kunci
    matching_books = Book.objects.filter(nama_buku__icontains=keyword)
    list_desc = []
    for i in matching_books:
        str = i.description
        str = str[0:100]
        list_desc.append(str)
    books_info = zip(matching_books,list_desc)

    context = {
        'keyword': keyword,
        'books':books_info,
    }

    return render(request, 'cari_buku.html', context)

def rekomen(request):
    user_profile = Profile.objects.get(user=request.user)  # Gantilah dengan cara Anda mengambil profil pengguna yang sesuai
    genre1 = user_profile.favorite_genre1
    genre2 = user_profile.favorite_genre2
    genre3 = user_profile.favorite_genre3

    # Gunakan operasi Q untuk menggabungkan beberapa kondisi OR
    matching_books = Book.objects.filter(
        Q(genre_1=genre1) | Q(genre_2=genre1) | Q(genre_3=genre1) | Q(genre_4=genre1) | Q(genre_5=genre1) |
        Q(genre_1=genre2) | Q(genre_2=genre2) | Q(genre_3=genre2) | Q(genre_4=genre2) | Q(genre_5=genre2) |
        Q(genre_1=genre3) | Q(genre_2=genre3) | Q(genre_3=genre3) | Q(genre_4=genre3) | Q(genre_5=genre3)
    )
    list_desc = []
    for i in matching_books:
        str = i.description
        str = str[0:100]
        list_desc.append(str)
    books_info = zip(matching_books,list_desc)

    context = {
        'books':books_info,
    }

    return render(request, 'rekomen.html', context)