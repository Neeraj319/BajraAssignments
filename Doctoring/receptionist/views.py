from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from core.forms import PatientCreationForm, AppointmentCreationForm
from django.views.generic import TemplateView
from django.views.generic.edit import DeleteView
from django.contrib import messages
from django.views.generic.list import ListView
from core.models import Patient, Appointment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from typing import Any
from Auth.mixins import IsReceptionistMixin
from django.db.models import QuerySet


class AppointmentListView(LoginRequiredMixin, IsReceptionistMixin, ListView):
    """
    This one is specific to the receptionist.
    Functionality according to the user are separated from
    receptionist's view and doctor's view
    """

    model: Appointment = Appointment
    template_name: str = "all_appointments.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["appointments"]: QuerySet[Appointment] = Appointment.objects.all()
        return context


class ReceptionistDashboard(LoginRequiredMixin, IsReceptionistMixin, TemplateView):
    template_name: str = "receptionist_dashboard.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        query_set: QuerySet[Patient] = Patient.objects.filter(appointment__isnull=True)
        context["patients"] = query_set
        return context


class PatientEditView(LoginRequiredMixin, IsReceptionistMixin, TemplateView):
    template_name: str = "patient_edit.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["patient"]: Patient = Patient.objects.get(pk=kwargs["pk"])
        context["form"]: PatientCreationForm = PatientCreationForm(
            instance=context["patient"]
        )
        return context

    def post(
        self, request: HttpRequest, *args, **kwargs
    ) -> HttpResponseRedirect | HttpResponse:
        patient: Patient = Patient.objects.get(pk=kwargs["pk"])
        form: PatientCreationForm = PatientCreationForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect("patient_detail", pk=kwargs["pk"])
        return self.get(request, *args, **kwargs)


class AppointmentCreationView(IsReceptionistMixin, LoginRequiredMixin, TemplateView):
    template_name: str = "appointment_creation.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        self.patient = Patient.objects.get(pk=self.kwargs["pk"])
        context["form"]: AppointmentCreationForm = AppointmentCreationForm()
        context["patient"]: Patient = self.patient
        return context

    def post(
        self, request: HttpRequest, *args, **kwargs
    ) -> HttpResponseRedirect | HttpResponse:
        form: AppointmentCreationForm = AppointmentCreationForm(request.POST)
        if form.is_valid():
            form.cleaned_data["patient"]: Patient = Patient.objects.get(
                pk=self.kwargs["pk"]
            )
            Appointment.objects.create(**form.cleaned_data)
            messages.success(
                self.request,
                "Your appointment request has been created successfully.",
            )
            return redirect("patient_detail", pk=self.kwargs["pk"])
        return self.get(request, *args, **kwargs)


class DeletePatientView(LoginRequiredMixin, IsReceptionistMixin, DeleteView):
    model: Patient = Patient
    success_url: str = "/"
    template_name: str = "patient_confirm_delete.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["patient"]: Patient = Patient.objects.get(pk=self.kwargs["pk"])
        return context

    def form_valid(self, form: PatientCreationForm) -> HttpResponseRedirect:
        messages.success(
            self.request,
            "Your patient record has been deleted successfully.",
        )
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return "/"
