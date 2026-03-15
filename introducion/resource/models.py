from django.db import models
from introducion.choises import ResourceStatus, ResourceType

# Create your models here.
class Resource(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=ResourceType.choices)
    status = models.CharField(
        max_length=20, 
        choices=ResourceStatus.choices, 
        default=ResourceStatus.AVAILABLE
    )
