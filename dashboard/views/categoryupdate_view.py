from dashboard.models.category_model import Category
from dashboard.mixin import AdminRequiredMixin
from django.views.generic import UpdateView
from django.contrib import messages
from dashboard.forms import CategoryForm
from django.urls import reverse_lazy


class CategoryUpdateView(AdminRequiredMixin, UpdateView):
    model = Category
    template_name = "dashboard/category_update.html"
    form_class = CategoryForm
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        messages.success(self.request, "Category updated successfully.")
        return super().form_valid(form)
