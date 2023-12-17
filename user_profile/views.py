import json
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from user_profile.forms import ProfileForm
from user_profile.models import Profile
from book_page.models import Book
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core import serializers

@csrf_exempt
@login_required
def profile(request):
    profile = request.user.profile
    if request.user.username == 'adminliterakarya':
        profile.first_name = 'admin'
        profile.last_name = 'literakarya'
        profile.bio = 'penguasa web'
        profile.address = 'balgebun'
        profile.favorite_genre1 = 'Fiction'
        profile.favorite_genre2 = 'Novels'
        profile.favorite_genre3 = 'Classics'
        profile.save()

        # Ambil seluruh username dari model User
        all_accounts = User.objects.all()
        
        # Redirect ke halaman allprofile.html dengan menyertakan data seluruh username
        return render(request, 'allprofile.html', {'all_accounts': all_accounts})
    
    else:
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


@csrf_exempt
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

@login_required
def delete_account(request, id):
    if request.method == "POST":
        account = User.objects.get(pk=id)
        account.delete()
    return HttpResponseRedirect(reverse('user_profile:profile'))

def get_json(request):
    profile = request.user.profile
    if profile.first_name is None:
            profile.first_name = 'Firstname'
            profile.last_name = 'Lastname'
            profile.bio = 'Bio'
            profile.address = 'Address'
            profile.favorite_genre1 = 'Fiction'
            profile.favorite_genre2 = 'Novels'
            profile.favorite_genre3 = 'Classics'
            profile.save()
    profiles = Profile.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize('json', profiles), content_type="application/json")

def get_allaccount_json(request):
    if request.user.username == "adminliterakarya":
        allaccount = User.objects.all()
    return HttpResponse(serializers.serialize('json', allaccount), content_type="application/json")

@csrf_exempt
def delete_account_flutter(request, id):
    if request.method == 'DELETE':  # Use DELETE instead of POST
        account = get_object_or_404(User, pk=id)
        account.delete()
        return JsonResponse({"status": "success"}, status=204)  # Status code changed to 204 for successful deletion
    else:
        return JsonResponse({"status": "error"}, status=405)  # 405 Method Not Allowed for other HTTP methods

@csrf_exempt
def create_profile_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_profile = Profile.objects.create(
            user = request.user,
            first_name = data["first_name"],
            last_name = data["last_name"],
            bio = data["bio"],
            address = data["address"],
            favorite_genre1 = data["favorite_genre1"],
            favorite_genre2 = data["favorite_genre2"],
            favorite_genre3 = data["favorite_genre3"],
        )
        new_profile.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
@csrf_exempt
def edit_profile_flutter(request, id):
    if request.method == 'POST':
        profile = get_object_or_404(Profile, pk=id, user=request.user)
        data = json.loads(request.body)
        profile.first_name = data.get('first_name', profile.first_name)
        profile.last_name = data.get('last_name', profile.last_name)
        profile.bio = data.get('bio', profile.bio)
        profile.address = data.get('address', profile.address)
        profile.favorite_genre1 = data.get('favorite_genre1', profile.favorite_genre1)
        profile.favorite_genre2 = data.get('favorite_genre2', profile.favorite_genre2)
        profile.favorite_genre3 = data.get('favorite_genre3', profile.favorite_genre3)
        profile.save()
        return JsonResponse({"status": "success"}, status=200)

    else:
        return JsonResponse({"status": "error"}, status=401)

