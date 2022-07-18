from django.urls import path
from .views import (
    ChangeAppointmentStatus,
    ChangeDoctorStatus,
    DoctorDashboard,
    DoctorListAllAppointments,
    IndexView,
    CreatePatientRecordView,
    return_to_dashboard,
    PatientDetailView,
)

urlpatterns = [
    path("", view=IndexView.as_view(), name="index"),
    path(
        "patient/create",
        view=CreatePatientRecordView.as_view(),
        name="create_patient",
    ),
    path(
        "dashboard",
        view=return_to_dashboard,
        name="dashboard",
    ),
    path(
        "patient/<int:pk>",
        view=PatientDetailView.as_view(),
        name="patient_detail",
    ),
    path(
        "doctor_dashboard",
        view=DoctorDashboard.as_view(),
        name="doctor_dashboard",
    ),
    path(
        "appointment/<int:pk>/change_status",
        view=ChangeAppointmentStatus.as_view(),
        name="appointment_change",
    ),
    path(
        "doctor/appointments",
        view=DoctorListAllAppointments.as_view(),
        name="doctor_appointments",
    ),
    path(
        "doctor/status/change",
        view=ChangeDoctorStatus.as_view(),
        name="doctor_status_change",
    ),
]
