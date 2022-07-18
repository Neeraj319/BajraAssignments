from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Receptionist(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneNumberField(null=True, blank=True)

    def __str__(self: "Receptionist") -> str:
        return f"{self.user.first_name} {self.user.last_name}"
