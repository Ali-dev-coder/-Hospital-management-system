from django.contrib import admin
from .models import Doctormodel,Patientmodel,Appointmentmodel
# Register your models here.
class doctoradmin(admin.ModelAdmin):
    pass
admin.site.register(Doctormodel,doctoradmin)

class patientadmin(admin.ModelAdmin):
    pass
admin.site.register(Patientmodel,patientadmin)

class appointmentadmin(admin.ModelAdmin):
    pass
admin.site.register(Appointmentmodel,appointmentadmin)
