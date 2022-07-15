from .forms import PatientCreationForm
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib import messages


# Create your views here.


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PatientCreationForm()
        return context


class CreatePatientRecordView(FormView):
    form_class = PatientCreationForm

    def form_valid(self, form: PatientCreationForm):
        form.save()
        messages.success(
            self.request,
            "Your appointment request has been created successfully. You should receive a confirmation email shortly.",
        )
        return super().form_valid(form)

    def get_success_url(self):
        return "/"
