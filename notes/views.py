from django.urls import reverse
from .models import Notes
from book_page.models import Book
from notes.forms import NoteForm
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404


@login_required(login_url='/login')
def show_notes(request):
    all_books = Book.objects.all().order_by('nama_buku')
    notes = Notes.objects.filter(user=request.user)

    if request.user.username == "adminliterakarya":
        context = {
            'all_books': all_books,
            'user': request.user.username,
            'notes': notes,
        }
        return render(request, "admin_notes_dashboard.html", context)
    
    else:
        context = {
            'all_books': all_books,
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
        buku = Book.objects.filter(nama_buku=judul_buku)
        
        new_note = Notes(
            # buku=buku,
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
    if request.user.username == "adminliterakarya":
        note_item = Notes.objects.all()
    else:
        note_item = Notes.objects.filter(user=request.user)
        
    return HttpResponse(serializers.serialize('json', note_item))

@csrf_exempt
def delete_note(request, id):
    if request.method == "DELETE":
        note = Notes.objects.get(pk=id)
        note.delete()
        return HttpResponse(b"DELETED", status=201)
    
    return HttpResponseNotFound()

def edit_note(request, id):
    note = Notes.objects.get(pk = id)
    books = Book.objects.all().order_by('nama_buku')

    # Set note sebagai instance dari form
    form = NoteForm(request.POST or None, instance=note)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('notes:show_notes'))

    context = {'form': form, 'books':books}
    return render(request, "edit_note.html", context)

def get_id(request, judul):
    buku = Book.objects.get(nama_buku=judul)
    buku_id = buku.pk
    return HttpResponse(buku_id)
    
    
    
