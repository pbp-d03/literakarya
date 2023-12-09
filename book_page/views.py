import json
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from book_page.models import Book, Comment, Bookmark
from book_page.forms import KomenForm

from django.contrib.auth.decorators import login_required

# Create your views here.
# @login_required(login_url='/login')
def get_books(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("json",data), content_type="application/json")

# @login_required(login_url='/login')
def show_list_books(request):
    buku = Book.objects.all()
    list_desc = []

    if request.method == 'POST':
        hasil_cari = request.POST['searched']
        buku = Book.objects.filter(genre_1__contains = hasil_cari) | Book.objects.filter(genre_2__contains = hasil_cari) | Book.objects.filter(genre_3__contains = hasil_cari) | Book.objects.filter(genre_4__contains = hasil_cari) | Book.objects.filter(genre_5__contains = hasil_cari)

    for i in buku:
        str = i.description
        str = str[0:100]
        list_desc.append(str)

    books_info = zip(buku,list_desc)     
    banyak_buku = len(buku)

    context = {
        'books':books_info,
        'banyak_buku':banyak_buku
    }
    return render(request,"tampilan_buku.html",context)

def show_filtered_flutter(request,hasil_cari):
    data = Book.objects.filter(genre_1__contains = hasil_cari) | Book.objects.filter(genre_2__contains = hasil_cari) | Book.objects.filter(genre_3__contains = hasil_cari) | Book.objects.filter(genre_4__contains = hasil_cari) | Book.objects.filter(genre_5__contains = hasil_cari)
    return HttpResponse(serializers.serialize("json",data), content_type="application/json")

# @login_required(login_url='/login')
def show_bookmark(request):
    bookmark = Bookmark.objects.filter(user=request.user)
    list_desc = []
    list_buku = []

    for j in bookmark:
        buku = j.buku
        list_buku.append(buku)
    
    list_set_buku = set(list_buku)
    list_buku = (list(list_set_buku))
    
    if request.method == "POST":
        hasil_cari = request.POST['hasil-book']
        list_search_buku = []
        for k in list_buku:
            if hasil_cari.lower() in k.nama_buku.lower():
                list_search_buku.append(k)
        list_buku = list_search_buku

    for i in list_buku:
        str = i.description
        str = str[0:100]
        list_desc.append(str)

    books_info = zip(list_buku,list_desc)   
    banyak_buku = len(list_buku)

    context = {
        'books':books_info,
        'banyak_buku':banyak_buku
    }
    
    return render(request,'bookmark.html',context)

# @login_required(login_url='/login')
@csrf_exempt
def add_bookmark_ajax(request,id):
    if request.method == 'POST':
        user = request.user
        buku = Book.objects.get(pk=id)
        new_bookmark = Bookmark(user = user, buku = buku)
        new_bookmark.save()

        return HttpResponse(b"CREATED", status=201)
    
    return HttpResponseNotFound()

# @login_required(login_url='/login')
def show_book(request,id):
    buku_pilihan = Book.objects.get(pk=id)
    bookmark = Bookmark.objects.filter(user=request.user)
    form = KomenForm()

    list_buku = []

    for j in bookmark:
        buku = j.buku
        list_buku.append(buku)
    
    list_set_buku = set(list_buku)
    list_buku = (list(list_set_buku))

    dibookmark = False
    for i in list_buku:
        if i.pk == id:
            dibookmark = True
            break
    
    context = {
        'book':buku_pilihan ,
        'form':form,
        'dibookmark':dibookmark,
        'idnext':id+1,
        'idprev':id-1
    }
    return render(request,"info_buku.html",context)

# @login_required(login_url='/login')
def get_komen_json(request,id1):
    buku = get_object_or_404(Book, pk = id1)
    komen_all = Comment.objects.filter(buku = buku)
    return HttpResponse(serializers.serialize('json', komen_all))

# @login_required(login_url='/login')
@csrf_exempt
def add_comment_ajax(request,id1):
    form = KomenForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            buku = get_object_or_404(Book, pk = id1)
            user = request.user.username
            isi_komen = request.POST.get('isi_komen')

            new_komen = Comment(user=user,buku=buku,isi_komen=isi_komen,likes=0,dislikes=0)
            new_komen.save()

            return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

@csrf_exempt
def create_komen_flutter(request,id):
    if request.method == 'POST':
        # print("TEST 1")
        data = json.loads(request.body)
        print(data)
        buku = get_object_or_404(Book, pk = id)
        user = request.user.username
        isi_komen = data["isi_komen"]

        new_komen = Comment(user=user,buku=buku,isi_komen=isi_komen,likes=0,dislikes=0)
        new_komen.save()
        
        # new_item = Item.objects.create(
        #     user = request.user,
        #     name = data["name"],
        #     amount = int(data["amount"]),
        #     description = data["description"],
        # )
        # # print(request.user, "ASAS")
        # # print("TEST 2")
        # new_item.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

# @login_required(login_url='/login')
@csrf_exempt
def delete_bookmark(request,id):
    if request.method == 'DELETE':
        buku_hapus_bookmark = Book.objects.get(pk = id)
        bookmark_hapus = Bookmark.objects.filter(buku = buku_hapus_bookmark).delete()
        return HttpResponse(b"DELETE", status=201)
    
    return HttpResponseNotFound()

# @login_required(login_url='/login')
@csrf_exempt
def add_likes(request,id):
    komen = Comment.objects.get(pk=id)
    komen.likes += 1
    # komen.likes = 0
    komen.save()
    return HttpResponse(b"CREATED", status=201)


# @login_required(login_url='/login')
@csrf_exempt
def delete_komen(request,id):
    if request.user.username != "adminliterakarya":
        return HttpResponseNotFound()
    
    print("MASUK")
    komen = Comment.objects.get(pk=id)
    komen.delete()
    return HttpResponse(b"DELETE", status=201)


