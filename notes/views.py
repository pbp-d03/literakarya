from django.urls import reverse
from .models import Note
from book_page.models import Book
from notes.forms import NoteForm
from django.http import HttpResponse, HttpResponseRedirect, QueryDict, JsonResponse, HttpResponseNotFound
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.shortcuts import get_object_or_404


@login_required(login_url='/login')
def show_notes(request):
    books = Book.objects.all().order_by('nama_buku')
    notes = Note.objects.filter(user=request.user)
    context = {
        'books': books,
        'user': request.user.username,
        'notes': notes,
    }
    return render(request, "notes.html", context)

@csrf_exempt         
def add_note(request):
    books = Book.objects.all().order_by('nama_buku')
    if request.method == 'POST':
        judul_catatan = request.POST.get("judul_catatan")
        judul_buku = request.POST.get("judul_buku")
        isi_catatan = request.POST.get("isi_catatan")
        penanda = request.POST.get("penanda")
        user=request.user
        
        new_note = Note(
            user=user,
            judul_catatan=judul_catatan,
            judul_buku=judul_buku,
            isi_catatan=isi_catatan,
            penanda=penanda,
        )
        
        new_note.save()
        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

def get_note_json(request):
    note_item = Note.objects.all()
    return HttpResponse(serializers.serialize('json', note_item))

@csrf_exempt
def delete_note(request, id):
    if request.method == "DELETE":
        note = Note.objects.get(pk=id)
        note.delete()
        return HttpResponse(b"DELETED", status=201)
    
    return HttpResponseNotFound()

def edit_note(request, id):
    note = Note.objects.get(pk = id)
    books = Book.objects.all().order_by('nama_buku')

    # Set note sebagai instance dari form
    form = NoteForm(request.POST or None, instance=note)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('notes:show_notes'))

    context = {'form': form, 'books':books}
    return render(request, "edit_note.html", context)