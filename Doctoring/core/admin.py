from django.contrib import admin

# Register your models here.
from .models import Patient, Doctor, Receptionist, Appointment

for model in [Patient, Doctor, Receptionist, Appointment]:
    admin.site.register(model)
