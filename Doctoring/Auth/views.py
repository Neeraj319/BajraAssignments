"""
all views are function based views cause 
it's easier to work with them in small features 
like login, logout and signup
"""
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from doctor.models import Doctor
from receptionist.models import Receptionist
from django.contrib.auth.models import User
from .helpers import get_form_data, validate_form_data


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


def signup_doctor(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if not request.user.is_authenticated:

        if request.method == "POST":
            form_data = get_form_data(request=request)
            if message := validate_form_data(
                username=form_data["username"],
                password=form_data["password"],
                confirm_password=form_data["confirm_password"],
                phone=form_data["phone"],
            ):
                messages.error(request, message)
                return redirect("signup")

            user = User.objects.create_user(
                username=form_data["username"],
                password=form_data["password"],
                first_name=form_data["first_name"],
                last_name=form_data["last_name"],
                email=form_data["email"],
            )
            Doctor.objects.create(
                user=user,
                phone=form_data["phone"],
                qualification=form_data["qualification"],
                years_practiced=form_data["years_practiced"],
                gender=form_data["gender"],
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
            form_data = get_form_data(request=request)
            if message := validate_form_data(
                username=form_data["username"],
                password=form_data["password"],
                confirm_password=form_data["confirm_password"],
                phone=form_data["phone"],
            ):
                messages.error(request, message)
                return redirect("signup")

            user: User = User.objects.create_user(
                username=form_data["username"],
                password=form_data["password"],
                first_name=form_data["first_name"],
                last_name=form_data["last_name"],
                email=form_data["email"],
            )
            Receptionist.objects.create(
                user=user,
                phone=form_data["phone"],
            )
            messages.success(
                request,
                "Your account has been created successfully",
            )
            return redirect("login")

        return redirect("login")
    else:
        return redirect("dashboard")
