from django.urls import path
from notes.views import (show_notes, add_note, delete_note, get_notes_json)

app_name = "notes_page"

urlpatterns = [
    path('', show_notes, name='show_notes'),
    path('add-note/', add_note, name='add_note'),
    path('delete-note/<int:id>', delete_note, name='delete_note'),
    path('json/all-notes/', get_notes_json, name="get_notes"),
]
