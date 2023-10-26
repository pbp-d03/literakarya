from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound, JsonResponse
from django.core import serializers
from ereading.models import Ereading
from book_page.models import Book
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url='/login')
def show_dashboard(request):
    books = Book.objects.all()
    context = {
        'books' : books,
    }
    return render(request, "ereading.html", context)

def get_json(request):
    ereadings = Ereading.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize('json', ereadings))

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
        ereading = Ereading.objects.filter(pk=id)
        ereading.delete()
        return HttpResponse(b"DELETED", status=201)
    
    return HttpResponseNotFound()