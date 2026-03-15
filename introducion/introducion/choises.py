from django.db import models
from django.utils.translation import gettext_lazy as _

class DependenceChoices(models.TextChoices):
    SYSTEMS = 'SYSTEMS', _('Sistemas')
    ADMINISTRATION = 'ADMINISTRATION', _('Administración')
    TEACHING = 'TEACHING', _('Docencia')
    EXTERNAL = 'EXTERNAL', _('Personal Externo')

class ResourceStatus(models.TextChoices):
    AVAILABLE = 'AVAILABLE', _('Disponible')
    RESERVED = 'RESERVED', _('Reservado')
    MAINTENANCE = 'MAINTENANCE', _('En Mantenimiento')
    DAMAGED = 'DAMAGED', _('Dañado/Fuera de servicio')

class ResourceType(models.TextChoices):
    ROOM = 'ROOM', _('Sala de reuniones')
    EQUIPMENT = 'EQUIPMENT', _('Equipo tecnológico')
    TOOL = 'TOOL', _('Herramienta manual')