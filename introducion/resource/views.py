from rest_framework import viewsets, permissions
from .models import Resource
from .serializers import ResourceSerializers
from authentication.permissions import IsSupervisorOrAdmin

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializers

    def get_permissions(self):
        if self.action in ['destroy', 'update', 'partial_update']:
            return [IsSupervisorOrAdmin()]
        
        # Para listar o ver un detalle, cualquier usuario logueado puede
        return [permissions.IsAuthenticated()]