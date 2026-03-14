from .models import Resource
from rest_framework import serializers

class ResourceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

        