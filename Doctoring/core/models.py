from django.db import models
from doctor.models import Doctor
from phonenumber_field.modelfields import PhoneNumberField


class Patient(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = PhoneNumberField(null=True, blank=True)
    email = models.EmailField()
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    issue = models.TextField(null=True)

    def __str__(self) -> str:
        return self.name


class Appointment(models.Model):
    patient: Patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    doctor: Doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    done = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.patient.name
