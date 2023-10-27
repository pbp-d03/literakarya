from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from user_profile.forms import ProfileForm
from user_profile.models import Profile

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

