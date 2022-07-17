"""
all views are function based views cause 
it's easier to work with them in small features 
like login, logout and signup
"""
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .models import Doctor, Receptionist
from django.contrib.auth.models import User


def login_user(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if not request.user.is_authenticated:

        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid username or password")
                return render(request, "login.html")

        return render(request, "login.html")
    else:
        return redirect("dashboard")


def signup(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if not request.user.is_authenticated:
        return render(request, "signup.html")
    else:
        return redirect("dashboard")


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


def signup_doctor(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if not request.user.is_authenticated:

        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            qualification = request.POST.get("qualification")
            years_practiced = request.POST.get("years_practiced")
            gender = request.POST.get.get("gender")

            if message := validate_form_data(
                username=username,
                password=password,
                confirm_password=confirm_password,
                phone=phone,
            ):
                messages.error(request, message)
                return redirect("signup")

            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            Doctor.objects.create(
                user=user,
                phone=phone,
                qualification=qualification,
                years_practiced=years_practiced,
                gender=gender,
            )
            messages.success(
                request,
                "Your account has been created successfully",
            )
            return redirect("login")

        return redirect("login")
    else:
        return redirect("dashboard")


def logout_user(request: HttpRequest) -> HttpResponseRedirect:
    logout(request)
    return redirect("login")


def signup_receptionist(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if not request.user.is_authenticated:

        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            phone = request.POST.get("phone")

            if message := validate_form_data(
                username=username,
                password=password,
                confirm_password=confirm_password,
                phone=phone,
            ):
                messages.error(request, message)
                return redirect("signup")

            user: User = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            Receptionist.objects.create(
                user=user,
                phone=phone,
            )
            messages.success(
                request,
                "Your account has been created successfully",
            )
            return redirect("login")

        return redirect("login")
    else:
        return redirect("dashboard")
