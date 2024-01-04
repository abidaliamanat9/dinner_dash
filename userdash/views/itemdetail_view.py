from django.views.generic import DetailView
from dashboard.models.item_model import Item


class ItemDetailView(DetailView):
    model = Item
    template_name = "userdash/item_detail.html"
    context_object_name = "item"
