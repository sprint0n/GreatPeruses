from django import forms
from .models import Book, UserBookRating

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'category', 'description', 'summary', 'cover']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = UserBookRating
        fields = ['rating', 'review', 'readingStatus']
        labels = {
            'readingStatus': 'Reading Status'
        }
        
