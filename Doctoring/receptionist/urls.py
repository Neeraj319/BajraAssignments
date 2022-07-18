from django.urls import path
from .views import (
    AppointmentCreationView,
    AppointmentListView,
    ReceptionistDashboard,
    PatientEditView,
    DeletePatientView,
)

urlpatterns = [
    path(
        "dashboard",
        view=ReceptionistDashboard.as_view(),
        name="receptionist_dashboard",
    ),
    path(
        "patient/<int:pk>/edit",
        view=PatientEditView.as_view(),
        name="patient_edit",
    ),
    path(
        "patient/<int:pk>/appointment/add",
        view=AppointmentCreationView.as_view(),
        name="patient_appointment_add",
    ),
    path(
        "patient/<int:pk>/delete",
        view=DeletePatientView.as_view(),
        name="patient_delete",
    ),
    path(
        "appointment/all",
        view=AppointmentListView.as_view(),
        name="all_appointments",
    ),
]
