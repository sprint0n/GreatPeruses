from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
# Create your models here.

class Book(models.Model):
    
    def __str__(self):
        return self.title

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=200, default='favorites')
    description = models.TextField(max_length=500)
    globalRating = models.FloatField(default=1.0)
    cover = models.ImageField(upload_to='images', default='images/none/noimg.jpg')
    summary = models.TextField(max_length=2000)
    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )

class UserBookRating(models.Model):

    READING_CHOICES = [
        ('u', 'Unread'),
        ('tr', 'To Read'),
        ('ip', 'Reading'),
        ('r', 'Read')

    ]
    user = models.ForeignKey('users.Profile', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.FloatField(
        null=True, 
        blank=True, 
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)]
    )
    review = models.TextField(max_length=500)
    readingStatus = models.CharField(max_length=2, choices=READING_CHOICES, default='u')

    class Meta:
        unique_together = ('user', 'book')
