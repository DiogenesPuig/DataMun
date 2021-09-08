from datetime import datetime
import django_filters

from .models import *
import datetime


class DiagnosticCasesFilter(django_filters.FilterSet):
    age = django_filters.ModelMultipleChoiceFilter(queryset=Age.objects.all())
    sex = django_filters.ModelMultipleChoiceFilter(queryset=Sex.objects.all())
    
    center = django_filters.ModelMultipleChoiceFilter(queryset=Center.objects.all())
    

    class Meta:
        model = DiagnosticCases
        fields = ['age', 'sex','center']
    


class WeekFilter(django_filters.FilterSet):
    class Meta:
        model = Week
        fields = ['year']

class DiagnosticFilter(django_filters.FilterSet):
    class Meta:
        model = Diagnostic
        fields = {
            'name': ['icontains'],
        }