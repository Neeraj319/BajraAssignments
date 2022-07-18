from django.contrib import admin

# Register your models here.
from .models import Patient, Appointment
from Auth.models import Doctor

for model in [Patient, Doctor, Appointment]:
    admin.site.register(model)
