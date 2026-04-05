from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import UserBookRating

@receiver([post_save, post_delete], sender=UserBookRating)
def update_book_ranking(sender, instance, **kwargs):
    book = instance.book
    avg = book.userbookrating_set.aggregate(Avg('rating'))['rating__avg']
    book.globalRating = avg or 1.0
    book.save()