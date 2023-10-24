from django.http import JsonResponse
from django.shortcuts import render
from book_page.models import Book
from .models import Post, Reply

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
                "user" : post.user.username,
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
                "user" : reply.user.username,
                "topic" : reply.topic,
                "body" : reply.body,
                "date" : reply.date.strftime("%B %d, %Y at %H:%M %Z")
            }
        })
    return JsonResponse(data,safe=False)

# # AJAX related
# @csrf_exempt
# def add_post(request):
#     if request.method == 'POST':
#         # retrieving data
#         pengguna = request.user
#         judul = request.POST.get('title')
#         isi = request.POST.get('body')
#         tanggal = timezone.now()
        
#         # making new instance and saving it
#         new_post = Post(
#             user = pengguna,
#             title = judul,
#             body = isi,
#             date = tanggal
#         )
#         new_post.save()
        
#         return JsonResponse({
#             "pk" : new_post.pk,
#             "fields" : {
#                 "user" : { 
#                         "username" : new_post.user.username,
#                         "name"     : new_post.user.name,
#                         "role"     : new_post.user.role
#                         },
#                 "title": new_post.title,
#                 "body" : new_post.body,
#                 "date" : new_post.date.strftime("%B %d, %Y at %H:%M %Z")
#             }
#         })
   
# @csrf_exempt         
# def add_comment(request, id):
#     if request.method == 'POST':
#         # retrieving data
#         post = Post.objects.get(pk=id)
#         pengguna = request.user
#         isi = request.POST.get('body')
#         tanggal = timezone.now()
        
#         # making new instance and save
#         new_comment = Comment(
#             post = post,
#             user = pengguna,
#             body = isi,
#             date = tanggal
#         )
#         new_comment.save()
        
#         return JsonResponse({
#             "pk" : new_comment.pk,
#             "fields" : {
#                 "post" : new_comment.post.id,
#                 "user" : { 
#                         "username" : new_comment.user.username,
#                         "name"     : new_comment.user.name,
#                         "role"     : new_comment.user.role
#                         },
#                 "body" : new_comment.body,
#                 "date" : new_comment.date.strftime("%B %d, %Y at %H:%M %Z")
#             }
#         })

# def delete_post(request, id):
#     this_post = Post.objects.get(pk=id)
#     this_post.delete()
#     return redirect('questions:show_questions')

# def delete_comment(request, id):
#     this_comment = Comment.objects.get(pk=id)
#     this_comment.delete()
#     return redirect('questions:show_questions')