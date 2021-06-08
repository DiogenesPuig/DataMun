from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Centro)
admin.site.register(Zona)
admin.site.register(Diagnostico)
admin.site.register(Semana)
admin.site.register(Paciente)

admin.site.register(Archivo)
