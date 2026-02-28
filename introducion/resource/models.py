from django.db import models

# Create your models here.
class Resource(models.model):
    name = models.TextField("Name")
    
