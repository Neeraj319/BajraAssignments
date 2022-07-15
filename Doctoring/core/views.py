from django.http import HttpRequest
from .forms import PatientCreationForm, AppointmentCreationForm
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.views.generic.list import ListView
from .models import Patient, Appointment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from typing import Any
from Auth.mixins import IsReceptionistMixin


def return_to_dashboard(request: HttpRequest):
    if hasattr(request.user, "receptionist"):
        return redirect("receptionist_dashboard")
    else:
        return redirect("doctor_dashboard")


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PatientCreationForm()
        return context

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if request.user.is_authenticated:
            return return_to_dashboard(request)
        else:
            return super(IndexView, self).dispatch(request, *args, **kwargs)


class CreatePatientRecordView(FormView):
    form_class = PatientCreationForm

    def form_valid(self, form: PatientCreationForm):
        form.save()
        messages.success(
            self.request,
            "Your appointment request has been created successfully. You should receive a confirmation email shortly.",
        )
        return super().form_valid(form)

    def get_success_url(self):
        return "/"


class PatientListView(LoginRequiredMixin, IsReceptionistMixin, ListView):
    model = Patient

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["appointments"] = Appointment.objects.filter(patient=self.object)
        return context


class ReceptionistDashboard(LoginRequiredMixin, IsReceptionistMixin, TemplateView):
    template_name = "receptionist_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["patients"] = Patient.objects.filter(appointment__isnull=True)
        return context


class PatientDetailView(LoginRequiredMixin, TemplateView):
    template_name = "patient_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["patient"] = Patient.objects.get(pk=kwargs["pk"])
        return context


class PatientEditView(LoginRequiredMixin, IsReceptionistMixin, TemplateView):
    template_name = "patient_edit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["patient"] = Patient.objects.get(pk=kwargs["pk"])
        context["form"] = PatientCreationForm(instance=context["patient"])
        return context

    def post(self, request, *args, **kwargs):
        patient = Patient.objects.get(pk=kwargs["pk"])
        form = PatientCreationForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect("patient_detail", pk=kwargs["pk"])
        return self.get(request, *args, **kwargs)


class AppointmentCreationView(IsReceptionistMixin, LoginRequiredMixin, FormView):
    template_name = "appointment_creation.html"
    form_class = AppointmentCreationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.patient = Patient.objects.get(pk=self.kwargs["pk"])
        context["form"] = AppointmentCreationForm()
        return context

    def form_is_valid(self, form):
        form["patient"] = self.patient
        form.save()
        return super().form_is_valid(form)

    def get_success_url(self) -> str:
        return "/patient/{}".format(self.kwargs["pk"])
