from django.shortcuts import render, redirect
from django.views import View
from dashboard.models.order_model import Order
from dashboard.models.cartitem_model import CartItem
from dashboard.mixin import AdminRequiredMixin
from django.contrib import messages
from django.db.models import F


class OrderDetailView(AdminRequiredMixin, View):
    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            cartitems = CartItem.objects.filter(user=order.user, order=order).annotate(
                stprice=F("quantity") * F("price")
            )
            total_items = sum(item.quantity for item in cartitems)
            total_price = sum(item.stprice for item in cartitems)
            return render(
                request,
                "dashboard/orderdetails.html",
                {
                    "order": order,
                    "cartitems": cartitems,
                    "total_items": total_items,
                    "total_price": total_price,
                },
            )
        except Order.DoesNotExist:
            messages.warning(request, "Order does not exist")
            return redirect("ordersdashboard")
