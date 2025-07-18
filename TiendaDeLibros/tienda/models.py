from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Libro(models.Model):
    GENEROS = [
        ('FIC', 'Ficción'),
        ('NOF', 'No Ficción'),
        ('FAN', 'Fantasía'),
        ('ROM', 'Romance'),
        ('TER', 'Terror'),
        ('INF', 'Infantil'),
        ('DEP', 'Deportes'),
    ]
    
    ESTADOS = [
        ('NUE', 'Nuevo'),
        ('USADO', 'Usado en buen estado'),
        ('DES', 'Desgastado'),
    ]
    
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    genero = models.CharField(max_length=3, choices=GENEROS)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    estado = models.CharField(max_length=5, choices=ESTADOS)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='libros/', blank=True, null=True)
    vendido = models.BooleanField(default=False)
    
    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    libro = models.ForeignKey(Libro, related_name='comentarios', on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Comentario de {self.autor} en {self.libro.titulo}'