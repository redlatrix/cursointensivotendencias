from rest_framework import viewsets
from .models import Resource
from .serializers import ResourceSerializers

# Create your views here.

class ResourcceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializers
