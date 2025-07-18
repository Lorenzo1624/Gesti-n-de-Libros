from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .models import Libro, Comentario
from .forms import LibroForm, ComentarioForm

def lista_libros(request):
    query = request.GET.get('q', '')
    if query:
        libros = Libro.objects.filter(titulo__icontains=query)
    else:
        libros = Libro.objects.all()
    return render(request, 'libros/lista_libros.html', {'libros': libros, 'query': query})

def detalle_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.libro = libro
            comentario.autor = request.user
            comentario.save()
            return redirect('detalle_libro', pk=libro.pk)
    else:
        form = ComentarioForm()
    return render(request, 'libros/detalle_libro.html', {'libro': libro, 'form': form})

@login_required
def agregar_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES)
        if form.is_valid():
            libro = form.save(commit=False)
            libro.vendedor = request.user
            libro.save()
            return redirect('detalle_libro', pk=libro.pk)
    else:
        form = LibroForm()
    return render(request, 'libros/agregar_libro.html', {'form': form})

@login_required
def mis_libros(request):
    libros = Libro.objects.filter(vendedor=request.user)
    return render(request, 'libros/mis_libros.html', {'libros': libros})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('lista_libros')
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = AuthenticationForm()
    return render(request, 'libros/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Autentica e inicia sesión automáticamente
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('lista_libros')
    else:
        form = UserCreationForm()
    return render(request, 'libros/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('lista_libros')

@login_required
def eliminar_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk, vendedor=request.user)
    if request.method == 'POST':
        libro.delete()
        return redirect('mis_libros')