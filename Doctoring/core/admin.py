from django.contrib import admin

# Register your models here.
from .models import Patient, Appointment

for model in [Patient, Appointment]:
    admin.site.register(model)
