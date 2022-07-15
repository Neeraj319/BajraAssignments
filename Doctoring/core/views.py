from django.shortcuts import render
from django.http import HttpRequest
from .forms import PatientCreationForm

# Create your views here.


def index(request: HttpRequest):
    form = PatientCreationForm()
    context = {
        "form": form,
    }
    return render(request, "index.html", context=context)
