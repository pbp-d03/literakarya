from django.urls import path
from notes.views import (show_notes, add_note, delete_note, get_note_json, edit_note, get_id)

app_name = "notes"

urlpatterns = [
    path('', show_notes, name='show_notes'),
    path('add-note/', add_note, name='add_note'),
    path('delete-note/<int:id>/', delete_note, name='delete_note'),
    path('get-note/', get_note_json, name="get_note_json"),
    path('edit-note/<int:id>/', edit_note, name='edit_note'),
    path('get-id/<str:judul>/', get_id, name='get_id')
    
]