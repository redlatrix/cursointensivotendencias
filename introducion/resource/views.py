from rest_framework import permissions, viewsets
from authentication.permissions import IsSupervisorOrAdmin
from .models import Resource, ResourceType, Assignment
from .serializers import (
    ResourceSerializers, 
    ResourceTypeSerializer, 
    AssignmentSerializer
)

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializers

    def get_permissions(self):
        if self.action in ["create", "destroy", "update", "partial_update"]:
            return [IsSupervisorOrAdmin()]
        return [permissions.IsAuthenticated()]

class ResourceTypeViewSet(viewsets.ModelViewSet):
    queryset = ResourceType.objects.all()
    serializer_class = ResourceTypeSerializer

    def get_permissions(self):
        if self.action in ["create", "destroy", "update", "partial_update"]:
            return [IsSupervisorOrAdmin()]
        return [permissions.IsAuthenticated()]

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    
    def get_permissions(self):
        if self.action in ["create", "destroy", "update", "partial_update"]:
            return [IsSupervisorOrAdmin()]
        return [permissions.IsAuthenticated()]
