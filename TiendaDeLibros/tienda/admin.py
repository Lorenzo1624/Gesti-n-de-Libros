from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Libro  # Asegúrate de importar tu modelo

admin.site.register(Libro)