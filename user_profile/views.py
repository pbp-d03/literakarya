from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from user_profile.models import Profile
from user_profile.forms import ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def show_profile(request):
    profiles = Profile.objects.filter(user=request.user)
    context = {
        'profiles': profiles,
    }
    return render(request, "profile.html", context)

def get_profile_json(request):
    items = Profile.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize('json', items))

@csrf_exempt
def create_profile(request):
    if request.method == "POST":
        user = request.user  # Mengambil pengguna yang masuk
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        bio = request.POST.get("bio")
        address = request.POST.get("address")
        favorite_genre1 = request.POST.get("favorite_genre1")
        favorite_genre2 = request.POST.get("favorite_genre2")
        favorite_genre3 = request.POST.get("favorite_genre3")
        
        # Membuat objek Profil Pengguna
        profile = Profile(user=user, first_name=first_name, last_name=last_name, bio=bio, address=address, favorite_genre1=favorite_genre1, favorite_genre2=favorite_genre2, favorite_genre3=favorite_genre3)
        profile.save()
        
        return JsonResponse({"message": "Profil Pengguna berhasil dibuat."})
    
    return JsonResponse({"message": "Permintaan tidak valid."})

@csrf_exempt
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return HttpResponse('Profile updated successfully.')
        else:
            return HttpResponse('Invalid form data.', status=400)

    return render(request, 'profile.html', {'form': ProfileForm(instance=request.user.profile)})