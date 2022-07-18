from django import forms
from .models import Patient, Appointment
from doctor.models import Doctor


class PatientCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PatientCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Patient
        fields = "__all__"

        widgets = {
            "date_of_birth": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={
                    "class": "form-control",
                    "placeholder": "Select a date",
                    "type": "date",
                },
            ),
            "issue": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your issue",
                }
            ),
        }


class AppointmentCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AppointmentCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
        self.fields["doctor"].queryset = Doctor.objects.filter(available=True)

    class Meta:
        model = Appointment
        fields = ["date", "time", "doctor"]

        widgets = {
            "date": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={
                    "class": "form-control",
                    "placeholder": "Select a date",
                    "type": "date",
                },
            ),
            "time": forms.TimeInput(
                format=("%H:%M"),
                attrs={
                    "class": "form-control",
                    "placeholder": "Select a time",
                    "type": "time",
                },
            ),
        }
