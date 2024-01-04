from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from dashboard.models.order_model import Order
from django.contrib.auth.mixins import LoginRequiredMixin


class MyOrdersView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("login")

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        return render(request, "userdash/myorders.html", {"orders": orders})
