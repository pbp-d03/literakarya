from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from user_profile.models import Profile
from user_profile.forms import ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
# Create your views here.

def show_profile(request):
    profiles = Profile.objects.all()

    context = {
        'profiles': profiles,
    }

    return render(request, "profile.html", context)

def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return HttpResponse('Profile updated successfully.')
        else:
            return HttpResponse('Invalid form data.', status=400)

    return render(request, 'profile.html', {'form': ProfileForm(instance=request.user.userprofile)})