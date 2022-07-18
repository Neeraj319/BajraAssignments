from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from .forms import PatientCreationForm
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib import messages
from .models import Patient
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from typing import Any
from django.db.models import QuerySet


def return_to_dashboard(request: HttpRequest):
    """
    this view is here to return logged in user to their
    specific dashboard page
    """
    if hasattr(request.user, "receptionist"):
        return redirect("receptionist_dashboard")
    else:
        return redirect("doctor_dashboard")


class IndexView(TemplateView):
    template_name: str = "index.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"]: PatientCreationForm = PatientCreationForm()
        return context

    def dispatch(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponseRedirect | HttpResponse:
        if request.user.is_authenticated:
            return return_to_dashboard(request)
        else:
            return super(IndexView, self).dispatch(request, *args, **kwargs)


class CreatePatientRecordView(FormView):
    form_class: PatientCreationForm = PatientCreationForm

    def form_valid(self, form: PatientCreationForm) -> HttpResponseRedirect:
        form.save()

        messages.success(
            self.request,
            "Your appointment request has been created successfully. You should receive a confirmation email shortly.",
        )
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return "/"


class PatientDetailView(LoginRequiredMixin, TemplateView):
    template_name: str = "patient_detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["patient"]: Patient = Patient.objects.get(pk=kwargs["pk"])

        return context
