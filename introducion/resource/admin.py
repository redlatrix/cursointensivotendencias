from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Resource

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'status') # Usa los nombres exactos de tu modelo
    list_filter = ('type', 'status')