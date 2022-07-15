from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Doctor(models.Model):
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    years_practiced = models.IntegerField()
    qualification = models.CharField(max_length=200)
    available = models.BooleanField(default=True, null=True)

    def __str__(self: "Doctor"):
        return f"{self.user.first_name} {self.user.last_name}"


class Receptionist(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)

    def __str__(self: "Receptionist"):
        return f"{self.user.first_name} {self.user.last_name}"
