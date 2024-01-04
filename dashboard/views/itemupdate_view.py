from dashboard.models.item_model import Item
from dashboard.mixin import AdminRequiredMixin
from django.views.generic import UpdateView
from django.contrib import messages
from dashboard.forms import ItemForm
from django.urls import reverse_lazy


class ItemUpdateView(AdminRequiredMixin, UpdateView):
    model = Item
    template_name = "dashboard/item_update.html"
    form_class = ItemForm
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        messages.success(self.request, "Item Updated successfully.")
        return super().form_valid(form)
