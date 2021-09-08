

from rest_framework import serializers
from .models import *

class CenterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Center
        fields = '__all__'

class DiagnosticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnostic
        fields = '__all__'

