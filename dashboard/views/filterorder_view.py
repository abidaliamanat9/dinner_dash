from django.shortcuts import render
from django.views import View
from dashboard.models.order_model import Order
from dashboard.mixin import AdminRequiredMixin


class FilterOrderView(AdminRequiredMixin, View):
    def get(self, request):
        action = request.GET.get("action", "ORDERED")
        orders = Order.objects.filter(status=action)
        return render(
            request, "dashboard/filterorders.html", {"orders": orders, "status": action}
        )
