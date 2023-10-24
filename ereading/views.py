from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from ereading.models import Ereading
from django.views.decorators.csrf import csrf_exempt

def show_dashboard(request):
    return render(request, "ereading.html")