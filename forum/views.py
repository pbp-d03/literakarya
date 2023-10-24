from django.http import JsonResponse
from django.shortcuts import redirect, render
from book_page.models import Book
from .models import Post, Reply
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

def show_forum(request):
    books = Book.objects.all()
    post = Post.objects.all()
    context = {
        'books' : books,
        'user' : request.user.username,
        'post' : post,
    }
    return render(request, "forum.html", context)

def get_posts_json(request):
    data = []
    posts = Post.objects.all()
    
    for post in posts:
        data.append({
            "pk" : post.pk,
            "fields" : {
                "user" : post.user,
                "subject" : post.subject,
                "topic" : post.topic,
                "message" : post.message,
                "date" : post.date.strftime("%B %d, %Y at %H:%M %Z")
            }
        })
    return JsonResponse(data,safe=False)

def get_replies_json(request):
    data = []
    replies = Reply.objects.all()
    
    for reply in replies:
        data.append({
            "pk" : reply.pk,
            "fields" : {
                "user" : reply.user,
                "topic" : reply.topic,
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
        kategori = request.POST.get('topik')
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
                "user" : new_post.user,
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
            topic = unggahan,
            body = komentar,
            date = tanggal
        )
        new_reply.save()
        
        return JsonResponse({
            "pk" : new_reply.pk,
            "fields" : {
                "user" : new_reply.user,
                "topic" : new_reply.topic,
                "body" : new_reply.body,
                "date" : new_reply.date.strftime("%B %d, %Y at %H:%M %Z")
            }
        })

def delete_post(request, id):
    post = Post.objects.get(pk=id)
    post.delete()
    return redirect('forum:show_forum')

def delete_reply(request, id):
    reply = Reply.objects.get(pk=id)
    reply.delete()
    return redirect('forum:show_forum')