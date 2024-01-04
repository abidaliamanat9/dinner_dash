from django.shortcuts import redirect
from django.views import View
from dashboard.models.order_model import Order
from dashboard.mixin import AdminRequiredMixin
from django.contrib import messages


class ModifyOrderView(AdminRequiredMixin, View):
    def get(self, request, order_id):
        action = request.GET.get("action", "PAID")
        try:
            order = Order.objects.get(pk=order_id)
            order.status = action
            order.save()
            messages.success(request, f"Order with id:{order_id} is {order.status}")
        except Order.DoesNotExist:
            messages.warning(request, "Order not exists")
        return redirect("ordersdashboard")
