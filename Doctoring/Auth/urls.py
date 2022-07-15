from django.urls import path
from .views import login_user, signup_doctor, signup, signup_receptionist

urlpatterns = [
    path("login/", login_user, name="login"),
    path("signup/", signup, name="signup"),
    path("signup/doctor/", signup_doctor, name="signup_doctor"),
    path("signup/receptionist/", signup_receptionist, name="signup_receptionist"),
]
