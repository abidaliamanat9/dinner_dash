from django.shortcuts import render
from django.views import View
from dashboard.models.cartitem_model import CartItem
from django.db.models import F


class MyCartView(View):
    def get(self, request):
        if request.user.is_authenticated and not request.user.is_staff:
            cart = CartItem.objects.filter(user=request.user, order=None).annotate(
                stprice=F("quantity") * F("price")
            )
            total_items = sum(item.quantity for item in cart)
            total_price = sum(item.stprice for item in cart)
        else:
            cart = request.session.get("cart", [])
            total_items = sum(item["quantity"] for item in cart)
            total_price = sum(item["stprice"] for item in cart)
        return render(
            request,
            "userdash/mycart.html",
            {"cart": cart, "total_items": total_items, "total_price": total_price},
        )
