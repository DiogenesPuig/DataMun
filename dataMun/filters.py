import django_filters
from .models import *

class PacienteFilter(django_filters.FilterSet):
    

    class Meta:
        model = Paciente
        fields = ['edad', 'sexo']
