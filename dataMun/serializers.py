

from rest_framework import serializers
from .models import *

class CenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Center
        fields = '__all__'




