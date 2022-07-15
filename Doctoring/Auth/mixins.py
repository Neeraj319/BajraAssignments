from django.http import HttpRequest
from django.shortcuts import redirect


class IsReceptionistMixin:
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            if hasattr(request.user, "receptionist"):
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect("doctor_dashboard")
        else:
            return redirect("login")


class IsDoctorMixin:
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            if hasattr(request.user, "doctor"):
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect("receptionist_dashboard")
        else:
            return redirect("login")
