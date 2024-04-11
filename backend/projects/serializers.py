from rest_framework import serializers
from .models import ImageAddress

class ImageAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageAddress
        fields = ['image', 'address']
        