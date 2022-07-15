from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Patient(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField()
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    issue = models.TextField(null=True)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self: "Doctor"):
        return f"{self.user.first_name} {self.user.last_name}"


class Receptionist(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self: "Receptionist"):
        return f"{self.user.first_name} {self.user.last_name}"


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.patient.name
