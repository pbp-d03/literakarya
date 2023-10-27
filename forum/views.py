from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from book_page.models import Book
from .models import Post, Reply
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

def show_forum(request):
    print("masuk forum")
    books = Book.objects.all()
    post = Post.objects.all()
    all_genres = Book.objects.values_list('genre_1', flat=True).distinct()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
        selected_genre = request.POST.get('selected_genre', None)
        print(selected_genre)
        if selected_genre == "Literasi umum":
            topic_options = [{'value': "Pilih Judul Buku", 'text': "Pilih Judul Buku"}]
            return JsonResponse({'topic_options': topic_options})
        if selected_genre:
            filtered_books = books.filter(genre_1=selected_genre)
            print(filtered_books)
        else:
            filtered_books = books

        topic_options = [{'value': book.nama_buku, 'text': book.nama_buku} for book in filtered_books]

        return JsonResponse({'topic_options': topic_options})

    context = {
        'books': books,
        'user': request.user.username,
        'post': post,
        'all_genres': all_genres,
    }

    return render(request, "forum.html", context)

def get_posts_json(request):
    data = []
    posts = Post.objects.all()
    
    for post in posts:
        data.append({
            "pk" : post.pk,
            "fields" : {
                "user" : post.user.username,
                "subject" : post.subject,
                "topic" : post.topic,
                "message" : post.message,
                "date" : post.date.strftime("%B %d, %Y at %H:%M %Z")
            }
        })
    return JsonResponse(data,safe=False)

def get_replies_json(request, id):
    data = []
    replies = Reply.objects.filter(post=id)
    
    for reply in replies:
        data.append({
            "pk" : reply.pk,
            "fields" : {
                "user" : reply.user.username,
                "post" : reply.post.id,
                "body" : reply.body,
                "date" : reply.date.strftime("%B %d, %Y at %H:%M %Z")
            }
        })
    return JsonResponse(data,safe=False)

# AJAX related
@csrf_exempt
def add_post(request):
    if request.method == 'POST':
        # ambil dari form
        op = request.user # op = original poster
        judul = request.POST.get('subject')
        kategori = request.POST.get('topic')
        pesan = request.POST.get('message')
        tanggal = timezone.now()
        
        # buat dan save post
        new_post = Post(
            user = op,
            subject = judul,
            topic = kategori,
            message = pesan,
            date = tanggal
        )
        new_post.save()
        
        return JsonResponse({
            "pk" : new_post.pk,
            "fields" : {
                "user" : new_post.user.username,
                "subject" : new_post.subject,
                "topic" : new_post.topic,
                "message" : new_post.message,
                "date" : new_post.date.strftime("%B %d, %Y at %H:%M %Z")
            }
        })
   
@csrf_exempt         
def add_reply(request, id):
    if request.method == 'POST':
        # ambil dari form
        penanggap = request.user
        unggahan = Post.objects.get(pk=id)
        komentar = request.POST.get('body')
        tanggal = timezone.now()
        
        # buat dan save reply
        new_reply = Reply(
            user = penanggap,
            post = unggahan,
            body = komentar,
            date = tanggal
        )
        new_reply.save()
        return JsonResponse({
            "pk" : new_reply.pk,
            "fields" : {
                "user" : new_reply.user.username,
                "post" : new_reply.post.id,
                "body" : new_reply.body,
                "date" : new_reply.date.strftime("%B %d, %Y at %H:%M %Z")
            }
        })

def delete_post(request, id):
    post = Post.objects.get(pk=id)
    post.delete()
    return HttpResponseRedirect(reverse('forum:show_forum'))

def delete_reply(request, id):
    reply = Reply.objects.get(pk=id)
    reply.delete()
    return HttpResponseRedirect(reverse('forum:show_forum'))