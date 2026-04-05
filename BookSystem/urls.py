from django.urls import path
from . import views

app_name = 'BookSystem' 

urlpatterns = [
    path('', views.book_list, name="books"),
    path('add/', views.add_book, name="add_book"),
    path('review/<int:pk>', views.review_book, name="review_book"),
    path('<int:pk>', views.book_detail, name="book_detail"),
    path('library/', views.book_library, name="book_library"),
    path('book/<int:pk>/update-status/', views.update_reading_status, name='update_status'),
   
]