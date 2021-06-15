import django_filters
from .models import *

class PacienteFilter(django_filters.FilterSet):
    

    class Meta:
        model = Paciente
        fields = ['edad', 'sexo']

class SemanaFilter(django_filters.FilterSet):
    

    class Meta:
        model = Semana
        fields = {
            'year': ['lt'],
        }
