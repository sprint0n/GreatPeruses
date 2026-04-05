from django.contrib import admin
from .models import Book, UserBookRating
# Register your models here.
admin.site.register(Book)

admin.site.register(UserBookRating)