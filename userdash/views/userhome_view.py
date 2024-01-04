from django.shortcuts import render
from django.views import View
from dashboard.models.category_model import Category
from dashboard.models.resturant_model import Resturant
from dashboard.models.item_model import Item


class UserHomeView(View):
    def get(self, request):
        resturants = Resturant.objects.all()
        categories = Category.objects.all()
        items = Item.objects.filter(retired=False)

        return render(
            request,
            "userdash/userhome.html",
            {"resturants": resturants, "categories": categories, "items": items},
        )
