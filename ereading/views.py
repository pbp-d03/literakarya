from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.core import serializers
from ereading.models import Ereading
from django.views.decorators.csrf import csrf_exempt

def show_dashboard(request):
    return render(request, "ereading.html")

def get_json(request):
    ereadings = Ereading.objects.all()
    return HttpResponse(serializers.serialize('json', ereadings))

@csrf_exempt
def add_ereading(request):
    print(request.POST)
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        description = request.POST.get("description")
        link = request.POST.get("link")

        ereading = Ereading(title=title, author=author, description=description, link=link)
        ereading.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

@csrf_exempt
def delete_ereading(request):
    if request.method=="POST":
        id = request.POST.get("id")
        ereading = Ereading.objects.get(pk=id)
        ereading.delete()
        
        return HttpResponse(b"DELETED", status=201)
    
    return HttpResponseNotFound()