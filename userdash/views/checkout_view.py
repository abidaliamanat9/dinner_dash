from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from dashboard.models.cartitem_model import CartItem, Order
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class CheckOutView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")

    def get(self, request):
        cartitems = CartItem.objects.filter(user=request.user, order=None)
        if cartitems.exists():
            order = Order.objects.create(user=request.user)
            cartitems.update(order=order)
            messages.success(request, "Your Order is placed successfuly")
        else:
            messages.warning(
                request, "You cart is empty! Order is not placed with empty cart"
            )
        return redirect("myorders")
