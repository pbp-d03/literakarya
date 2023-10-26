from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect
from django.urls import reverse
from book_page.models import Book
from .models import Note
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

def show_notes(request):
    books = Book.objects.all()
    notes = Note.objects.all()
    context = {
        'books': books,
        'user': request.user.username,
        'notes': notes,
    }
    return render(request, "notes.html", context)

def get_notes_json(request):
    data = []
    notes = Note.objects.all()
    
    for note in notes:
        data.append({
            "pk": note.pk,
            "fields": {
                "user": note.user.username,
                "message": note.message,
                "date": note.date.strftime("%B %d, %Y at %H:%M %Z")
            }
        })
    return JsonResponse(data, safe=False)

# AJAX related
@csrf_exempt         
def add_note(request):
    if request.method == 'POST':
        note_title = request.POST.get('judul_catatan')
        book_title = request.POST.get('judul_buku')
        note_content = request.POST.get('catatan')
        tag = request.POST.get('penanda')
        date = timezone.now()
        
        new_note = Note(
            user=request.user,
            judul_catatan=note_title,
            judul_buku=book_title,
            catatan=note_content,
            penanda=tag,
            date=date,
        )
        
        new_note.save()
        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

def delete_note(request, id):
    note = Note.objects.get(pk=id)
    note.delete()
    return HttpResponseRedirect(reverse('show_notes'))