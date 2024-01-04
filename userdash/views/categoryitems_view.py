from django.shortcuts import render
from django.views import View
from dashboard.models.category_model import Category
from dashboard.models.resturant_model import Resturant

from dashboard.models.item_model import Item


class CategoryItemsView(View):
    def get(self, request, cg_id):
        resturants = Resturant.objects.all()
        categories = Category.objects.all()
        items = Item.objects.filter(category__id=cg_id)
        if request.user.is_authenticated and request.user.is_staff:
            return render(
                request,
                "dashboard/dashboard.html",
                {"resturants": resturants, "categories": categories, "items": items},
            )
        else:
            return render(
                request,
                "userdash/userhome.html",
                {"resturants": resturants, "categories": categories, "items": items},
            )
