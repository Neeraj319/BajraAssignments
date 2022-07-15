from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.http import HttpRequest
from django.contrib import messages


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
