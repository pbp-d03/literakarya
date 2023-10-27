from django.urls import path
from notes.views import (show_notes, add_note, delete_note, edit_note, create_note, get_notes_json)

app_name = "notes_page"

urlpatterns = [
    path('', show_notes, name='show_notes'),
    path('add-note/', add_note, name='add_note'),
    path('edit-note/<int:id>', edit_note, name='edit_note'),
    path('create-note/', create_note, name='create_note'),
    path('delete-note/<int:id>', delete_note, name='delete_note'),
    path('get-notes/', get_notes_json, name="get_notes_json"),

]
