from django.urls import path
from .views import (
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
]
