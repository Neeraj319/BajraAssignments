import imp
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from .forms import PatientCreationForm, AppointmentCreationForm
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, DeleteView
from django.contrib import messages
from django.views.generic.list import ListView
from .models import Patient, Appointment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from typing import Any
from Auth.mixins import IsDoctorMixin, IsReceptionistMixin
from Auth.models import Doctor
from django.db.models import QuerySet


def return_to_dashboard(request: HttpRequest):
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


class AppointmentListView(LoginRequiredMixin, IsReceptionistMixin, ListView):
    model: Appointment = Appointment
    template_name: str = "all_appointments.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["appointments"]: Appointment = Appointment.objects.all()
        return context


class ReceptionistDashboard(LoginRequiredMixin, IsReceptionistMixin, TemplateView):
    template_name: str = "receptionist_dashboard.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        query_set = Patient.objects.filter(appointment__isnull=True)
        context["patients"]: Patient = query_set
        return context


class PatientDetailView(LoginRequiredMixin, TemplateView):
    template_name: str = "patient_detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["patient"]: Patient = Patient.objects.get(pk=kwargs["pk"])

        return context


class PatientEditView(LoginRequiredMixin, IsReceptionistMixin, TemplateView):
    template_name = "patient_edit.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["patient"]: Patient = Patient.objects.get(pk=kwargs["pk"])
        context["form"]: PatientCreationForm = PatientCreationForm(
            instance=context["patient"]
        )
        return context

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect | HttpResponse:
        patient: Patient = Patient.objects.get(pk=kwargs["pk"])
        form: PatientCreationForm = PatientCreationForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect("patient_detail", pk=kwargs["pk"])
        return self.get(request, *args, **kwargs)


class AppointmentCreationView(IsReceptionistMixin, LoginRequiredMixin, TemplateView):
    template_name = "appointment_creation.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        self.patient = Patient.objects.get(pk=self.kwargs["pk"])
        context["form"]: AppointmentCreationForm = AppointmentCreationForm()
        context["patient"]: Patient = self.patient
        return context

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect | HttpResponse:
        form: AppointmentCreationForm = AppointmentCreationForm(request.POST)
        if form.is_valid():
            form.cleaned_data["patient"] = Patient.objects.get(pk=self.kwargs["pk"])
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

    def delete(self, request, *args, **kwargs) -> HttpResponse:
        messages.success(
            self.request,
            "Your patient record has been deleted successfully.",
        )
        return super().delete(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return "/"


class DoctorDashboard(LoginRequiredMixin, IsDoctorMixin, TemplateView):
    template_name: str = "doctor_dashboard.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["appointments"]: QuerySet[Appointment] = Appointment.objects.filter(
            doctor=self.request.user.doctor, done=False
        )
        return context


class ChangeAppointmentStatus(LoginRequiredMixin, IsDoctorMixin, TemplateView):
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["appointment"]: Appointment = Appointment.objects.get(
            pk=self.kwargs["pk"]
        )
        return context

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        appointment = Appointment.objects.get(pk=self.kwargs["pk"])
        appointment.done = not appointment.done
        appointment.save()
        return redirect("doctor_dashboard")


class DoctorListAllAppointments(LoginRequiredMixin, IsDoctorMixin, TemplateView):
    template_name = "doctor_appointments.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["appointments"]: QuerySet[Appointment] = Appointment.objects.filter(
            doctor=self.request.user.doctor
        )
        return context


class ChangeDoctorStatus(LoginRequiredMixin, IsDoctorMixin, TemplateView):
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["doctor"] = Doctor.objects.get(pk=self.kwargs["pk"])
        return context

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        doctor = request.user.doctor
        doctor.available = not doctor.available
        doctor.save()
        return redirect("doctor_dashboard")
