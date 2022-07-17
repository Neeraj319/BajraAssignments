from django.urls import path
from .views import (
    AppointmentCreationView,
    AppointmentListView,
    IndexView,
    CreatePatientRecordView,
    return_to_dashboard,
    ReceptionistDashboard,
    PatientDetailView,
    PatientEditView,
    DeletePatientView,
)

urlpatterns = [
    path("", view=IndexView.as_view(), name="index"),
    path(
        "patient",
        view=CreatePatientRecordView.as_view(),
        name="patient",
    ),
    path(
        "dashboard",
        view=return_to_dashboard,
        name="dashboard",
    ),
    path(
        "receptionist/dashboard",
        view=ReceptionistDashboard.as_view(),
        name="receptionist_dashboard",
    ),
    path(
        "patient/<int:pk>",
        view=PatientDetailView.as_view(),
        name="patient_detail",
    ),
    path(
        "patient/<int:pk>/edit",
        view=PatientEditView.as_view(),
        name="patient_edit",
    ),
    path(
        "patient/<int:pk>/appointment/edit",
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
