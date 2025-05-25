from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Book, Order
from .forms import BookForm

def book_list(request):
    books = Book.objects.all()
    return render(request, 'store/book_list.html', {'books': books})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'store/book_detail.html', {'book': book})

@login_required
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.seller = request.user
            book.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'store/book_form.html', {'form': form})

@login_required
def order_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    Order.objects.create(book=book, buyer=request.user)
    return redirect('book_list')


