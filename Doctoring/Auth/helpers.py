from django.contrib.auth.models import User
from typing import Any
from django.http import HttpRequest


def validate_form_data(
    username: str, password: str, confirm_password: str, phone: str
) -> str | None:

    if User.objects.filter(username=username).first():
        return "Username already exists"
    if password != confirm_password:
        return "Passwords do not match"
    if len(password) < 8:
        return "Password must be at least 8 characters"
    if len(phone) > 15:
        return "Phone number must be smaller than 15 digits"


def get_form_data(request: HttpRequest) -> dict[str, Any]:
    form_data = dict()
    for key, value in request.POST.dict().items():
        if key == "csrfmiddlewaretoken":
            continue
        form_data[key] = value
    return form_data
