from django.http import HttpRequest, HttpResponseRedirect
from django.views.generic import TemplateView
from core.models import Appointment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from typing import Any
from Auth.mixins import IsDoctorMixin
from .models import Doctor
from django.db.models import QuerySet


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

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponseRedirect:
        appointment: Appointment = Appointment.objects.get(pk=self.kwargs["pk"])
        appointment.done = not appointment.done
        appointment.save()
        return redirect("doctor_dashboard")


class DoctorListAllAppointments(LoginRequiredMixin, IsDoctorMixin, TemplateView):
    template_name: str = "doctor_appointments.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["appointments"]: QuerySet[Appointment] = Appointment.objects.filter(
            doctor=self.request.user.doctor
        )
        return context


class ChangeDoctorStatus(LoginRequiredMixin, IsDoctorMixin, TemplateView):
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["doctor"]: Doctor = Doctor.objects.get(pk=self.kwargs["pk"])
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponseRedirect:
        doctor: Doctor = request.user.doctor
        doctor.available = not doctor.available
        doctor.save()
        return redirect("doctor_dashboard")
