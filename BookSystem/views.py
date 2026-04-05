from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, UserBookRating
from django.core.paginator import Paginator
from .forms import ReviewForm, BookForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

def perform_filtering_and_paging(request, queryset, is_library_view=False):
    categories = Book.objects.values_list('category', flat=True).distinct()
    
    book_title = request.GET.get('book_title')
    if book_title:
        queryset = queryset.filter(title__icontains=book_title)

    category_filter = request.GET.get('category_select')
    if category_filter:
        queryset = queryset.filter(category=category_filter)

    status_filter = request.GET.get('status_select')
    if status_filter:
        queryset = queryset.filter(userbookrating__readingStatus=status_filter).distinct()

    rating_filter = request.GET.get('rating_select')
    if rating_filter:
        if is_library_view:
            queryset = queryset.filter(
                userbookrating__user=request.user.profile, 
                userbookrating__rating__gte=rating_filter
            ).distinct()
        else:
            queryset = queryset.filter(globalRating__gte=rating_filter)

    paginator = Paginator(queryset, 8)
    page = request.GET.get('page')
    book_object = paginator.get_page(page)

    return render(request, 'Book/all-books.html', {
        'book_object': book_object, 
        'categories': categories,
        'is_library': is_library_view 
    })

@login_required
def book_list(request):
    books_queryset = Book.objects.all()
    return perform_filtering_and_paging(request, books_queryset, is_library_view=False)

@login_required
def book_library(request):
    books_queryset = Book.objects.filter(
        Q(uploader=request.user) | Q(userbookrating__user=request.user.profile)
    ).distinct()

    return perform_filtering_and_paging(request, books_queryset, is_library_view=True)

@login_required
def add_book(request):
    if request.method == "POST":
        book_form = BookForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)

        if book_form.is_valid():
            new_book = book_form.save(commit=False)
            new_book.uploader = request.user
            new_book.save()
            
            if review_form.is_valid() and request.POST.get('rating'):
                review = review_form.save(commit=False)
                review.book = new_book
                review.user = request.user.profile 
                review.save()
                
            messages.success(request, "Book added successfully!")
            return redirect('BookSystem:books')
    else:
        book_form = BookForm()
        review_form = ReviewForm()
    
    return render(request, 'Book/book-form.html', {
        'book_form': book_form,
        'review_form': review_form
    })

@login_required
def review_book(request, pk):
    book = get_object_or_404(Book, id=pk)
    existing_review = UserBookRating.objects.filter(user=request.user.profile, book=book).first()

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user.profile
            review.save()
            messages.success(request, "Review updated!")
            return redirect('BookSystem:books')
    else:
        form = ReviewForm(instance=existing_review)

    return render(request, 'Book/review-form.html', {
        'review_form': form, 
        'book': book
    })

@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, id=pk)
    reviews = UserBookRating.objects.filter(book=book)
    
    user_review = None
    if request.user.is_authenticated:
        user_review = UserBookRating.objects.filter(book=book, user=request.user.profile).first()

    return render(request, 'Book/book-detail.html', {
        'book': book,
        'reviews': reviews,
        'user_review': user_review,
    })

@login_required
def update_reading_status(request, pk):
    if request.method == "POST":
        book = get_object_or_404(Book, id=pk)
        status = request.POST.get('status')
        
        review, created = UserBookRating.objects.get_or_create(
            book=book, 
            user=request.user.profile 
        )
        
        review.readingStatus = status
        review.save() 
        
        messages.success(request, "Status updated!")
        
    return redirect('BookSystem:book_detail', pk=pk)