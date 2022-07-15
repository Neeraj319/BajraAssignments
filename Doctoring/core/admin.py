from django.contrib import admin

# Register your models here.
from .models import Patient, Appointment
from Auth.models import Receptionist, Doctor

for model in [Patient, Doctor, Receptionist, Appointment]:
    admin.site.register(model)
