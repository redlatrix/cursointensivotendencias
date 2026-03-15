from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def setConfigNewUser(sender, instance, created, **kwargs):
    if created:
        # 1. Creamos el perfil (contexto global de datos adicionales)
        Profile.objects.create(user=instance)
        
        # 2. Asignamos el rol por defecto (Control de acceso)
        try:
            # El grupo 'Estándar' debe existir en tu base de datos
            standarGroup = Group.objects.get(name='Estándar')
            instance.groups.add(standarGroup)
        except Group.DoesNotExist:
            # Si el grupo no existe, podrías crearlo o ignorarlo
            pass