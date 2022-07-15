from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.http import HttpRequest
from django.contrib import messages
from .models import Doctor, Receptionist
from django.contrib.auth.models import User


def login_user(request: HttpRequest):
    if not request.user.is_authenticated:

        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
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


def signup(request: HttpRequest):
    if not request.user.is_authenticated:
        return render(request, "signup.html")
    else:
        return redirect("dashboard")


def signup_doctor(request: HttpRequest):
    if not request.user.is_authenticated:

        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            confirm_password = request.POST["confirm_password"]
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            email = request.POST["email"]
            phone = request.POST["phone"]
            qualification = request.POST["qualification"]
            years_practiced = request.POST["years_practiced"]
            gender = request.POST.get("gender")

            if User.objects.filter(username=username).first():
                messages.error(request, "Username already exists")
                return redirect("signup")
            else:
                if password != confirm_password:
                    messages.error(request, "Passwords do not match")
                    return render(request, "signup.html")
                if len(password) < 8:
                    messages.error(request, "Password must be at least 8 characters")
                    return render(request, "signup.html")
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
