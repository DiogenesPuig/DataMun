from django.contrib import admin
from .models import *


class CenterAdmin(admin.ModelAdmin):
    list_display = ('code','name','coordinate','zone')

class ZoneAdmin(admin.ModelAdmin):
    list_display = ('code',)

class DiagnosticAdmin(admin.ModelAdmin):
    list_display = ('code','name',)


class DiagnosticCasesAdmin(admin.ModelAdmin):
    list_display = ('sex','age','diagnostic','center','cases','week')
    list_filter = ('sex','age','diagnostic','center','week')

class WeekAdmin(admin.ModelAdmin):
    list_display = ('year','week',)

# Register your models here.
admin.site.register(Center,CenterAdmin)
admin.site.register(Zone,ZoneAdmin)
admin.site.register(Diagnostic,DiagnosticAdmin)
admin.site.register(Week,WeekAdmin)
admin.site.register(DiagnosticCases,DiagnosticCasesAdmin)
admin.site.register(SpreadSheet)
admin.site.register(Coordinate)


admin.site.site_header = "DaMu administracion de la provincio de cordoba"