from django.urls import path
from .views import (
    ChangeAppointmentStatus,
    ChangeDoctorStatus,
    DoctorDashboard,
    DoctorListAllAppointments,
)

urlpatterns = [
    path(
        "dashboard",
        view=DoctorDashboard.as_view(),
        name="doctor_dashboard",
    ),
    path(
        "appointment/<int:pk>/change_status",
        view=ChangeAppointmentStatus.as_view(),
        name="appointment_change",
    ),
    path(
        "appointments",
        view=DoctorListAllAppointments.as_view(),
        name="doctor_appointments",
    ),
    path(
        "status/change",
        view=ChangeDoctorStatus.as_view(),
        name="doctor_status_change",
    ),
]
