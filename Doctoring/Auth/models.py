from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Doctor(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self: "Doctor"):
        return f"{self.user.first_name} {self.user.last_name}"


class Receptionist(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self: "Receptionist"):
        return f"{self.user.first_name} {self.user.last_name}"
