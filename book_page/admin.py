from django.contrib import admin
from .models import Book, Comment, Bookmark

# Register your models here.
admin.site.register(Book)
admin.site.register(Comment)
admin.site.register(Bookmark)