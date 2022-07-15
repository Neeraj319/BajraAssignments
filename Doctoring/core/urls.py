from django.urls import path
from .views import (
    IndexView,
    CreatePatientRecordView,
    return_to_dashboard,
    ReceptionistDashboard,
    PatientDetailView,
)

urlpatterns = [
    path("", view=IndexView.as_view(), name="index"),
    path("patient", view=CreatePatientRecordView.as_view(), name="patient"),
    path("dashboard", view=return_to_dashboard, name="dashboard"),
    path(
        "receptionist/dashboard",
        view=ReceptionistDashboard.as_view(),
        name="receptionist_dashboard",
    ),
    path("patient/<int:pk>", view=PatientDetailView.as_view(), name="patient_detail"),
]
