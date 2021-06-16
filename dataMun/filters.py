from datetime import datetime
import django_filters

from .models import *
import datetime



ages = [( '<1','<1 año'),
    ( '1 a 5','1 a 5 años'),
    ( '6 a 9','6 a 9 años'),
    ( '10 a 14','10 a 14 años'),
    ('15 a 19','15 a 19 años'),
    ('20 a 54 ','20 a 54 años'),
    ('55 a 64','55 a 64 años'),
    ('65 y mas','65 y mas años')]
sex = (
       ('M', ('Masculino')),
       ('F', ('Femenino')),
       )
class DiagnosticCasesFilter(django_filters.FilterSet):
    age = django_filters.MultipleChoiceFilter(choices=ages)
    sex = django_filters.MultipleChoiceFilter(choices=sex)
    week = django_filters.ModelMultipleChoiceFilter(queryset=Week.objects.filter(year=datetime.datetime.now().year))
    center = django_filters.ModelMultipleChoiceFilter(queryset=Center.objects.all())
    

    class Meta:
        model = DiagnosticCases
        fields = ['age', 'sex','center','week']
    


class WeekFilter(django_filters.FilterSet):
    class Meta:
        model = Week
        fields = {
            'year': ['lt'],
        }

