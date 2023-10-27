from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseNotFound
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from book_page.models import Book, Komen

# Create your views here.
def get_books(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("json",data), content_type="application/json")

def show_list_books(request):
    buku = Book.objects.all()
    list_desc = []
    for i in buku:
        str = i.description
        str = str[0:100]
        list_desc.append(str)

    books_info = zip(buku,list_desc)

    context = {
        'books':books_info,
    }
    return render(request,"tampilan_buku.html",context)

def show_book(request,id):
    buku = Book.objects.get(pk=id)
    context = {
        'book':buku
    }
    return render(request,"info_buku.html",context)


def get_komen_json(request,id1):
    buku = get_object_or_404(Book, pk = id1)
    komen_all = Komen.objects.filter(buku = buku)
    return HttpResponse(serializers.serialize('json', komen_all))

@csrf_exempt
def add_comment_ajax(request,id1):
    # Komen.objects.all().delete()
    if request.method == 'POST':
        buku = get_object_or_404(Book, pk = id1)
        user = request.user
        isi_komen = request.POST.get("isi_komen")

        new_komen = Komen(user=user,buku=buku,isi_komen=isi_komen,likes=0,dislikes=0)
        new_komen.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()


