from dashboard.models.resturant_model import Resturant
from dashboard.mixin import AdminRequiredMixin
from django.views.generic import CreateView
from django.contrib import messages
from dashboard.forms import ResturantForm
from django.urls import reverse_lazy


class ResturantCreateView(AdminRequiredMixin, CreateView):
    model = Resturant
    template_name = "dashboard/resturant_create.html"
    form_class = ResturantForm
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        messages.success(self.request, "Resturant created successfully.")
        return super().form_valid(form)
