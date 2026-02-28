from django.db import models

# Create your models here.
class Estante(models.Model):
    nombre = models.CharField(max_length=100)
    piso = models.CharField(max_length=50, help_text="Ej: Pasillo A, Planta 2")

    def __str__(self):
        return f"{self.nombre} ({self.piso})"


class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    año = models.DateField()
    stock = models.IntegerField(default=0)
    
    estante = models.ForeignKey(Estante, on_delete=models.SET_NULL, null=True, blank=True, related_name='libros')

    def __str__(self):
        return self.titulo