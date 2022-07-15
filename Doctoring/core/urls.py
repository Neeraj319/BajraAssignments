from django.urls import path
from .views import IndexView, CreatePatientRecordView

urlpatterns = [
    path("", view=IndexView.as_view(), name="index"),
    path("patient", view=CreatePatientRecordView.as_view(), name="patient"),
]
