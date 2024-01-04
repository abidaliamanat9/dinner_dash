from django.shortcuts import render
from django.views import View
from dashboard.models.cartitem_model import CartItem
from django.contrib import messages
from django.db.models import Count
from dashboard.models.category_model import Category
from dashboard.models.resturant_model import Resturant

from dashboard.models.item_model import Item


class PopularItemView(View):
    def get(self, request):
        resturants = Resturant.objects.all()
        categories = Category.objects.all()
        item_dict = (
            CartItem.objects.values("item__title")
            .annotate(max=Count("item__title"))
            .order_by("-max")
            .first()
        )
        try:
            items = Item.objects.filter(title=item_dict["item__title"])
        except Exception:
            messages.warning(request, "There is no order placed by any user yet")
        finally:
            return render(
                request,
                "userdash/userhome.html",
                {"resturants": resturants, "categories": categories, "items": items},
            )
