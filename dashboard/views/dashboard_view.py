from dashboard.models.resturant_model import Resturant
from dashboard.models.item_model import Item
from dashboard.models.category_model import Category
from dashboard.mixin import AdminRequiredMixin
from django.views import View
from django.shortcuts import render


class DashboardView(AdminRequiredMixin, View):
    def get(self, request):
        resturants = Resturant.objects.all()
        categories = Category.objects.all()
        items = Item.objects.all()

        return render(
            request,
            "dashboard/dashboard.html",
            {"resturants": resturants, "categories": categories, "items": items},
        )
