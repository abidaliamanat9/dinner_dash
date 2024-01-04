from django.shortcuts import render
from django.views import View
from dashboard.models.category_model import Category
from dashboard.models.resturant_model import Resturant

from dashboard.models.item_model import Item


class ResturantItemsView(View):
    def get(self, request, rest_id):
        resturants = Resturant.objects.all()
        categories = Category.objects.all()
        items = Item.objects.filter(resturant__id=rest_id)
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
