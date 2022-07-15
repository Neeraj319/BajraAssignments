from django import forms
from .models import Patient


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
