from django.db import models
from django.contrib.auth.models import User
from introducion.choises import DependenceChoices

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phonenumber = models.CharField(max_length=15, blank=True, null=True)
    identitydocument = models.CharField(max_length=20, unique=True, null=True, blank=True)
    dependence = models.CharField( # Antes era dependencia
        max_length=100,
        choices=DependenceChoices.choices,
        default=DependenceChoices.SYSTEMS
    )

    avatar = models.ImageField(upload_to='profiles/', null=True, blank=True)
    bibliography = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"