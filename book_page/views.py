from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers

from book_page.models import Book

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
        'buku':buku
    }
    return render(request,"info_buku.html",context)
