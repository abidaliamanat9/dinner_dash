from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView
from dashboard.models.cartitem_model import CartItem, Order
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import F


class OrderDetailView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("login")

    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            cartitems = CartItem.objects.filter(
                user=request.user, order=order
            ).annotate(stprice=F("quantity") * F("price"))
            total_items = sum(item.quantity for item in cartitems)
            total_price = sum(item.stprice for item in cartitems)
            return render(
                request,
                "userdash/myorder_details.html",
                {
                    "order": order,
                    "cartitems": cartitems,
                    "total_items": total_items,
                    "total_price": total_price,
                },
            )
        except Order.DoesNotExist:
            messages.warning(request, "You only have access to your oders")
            return redirect("myorders")
