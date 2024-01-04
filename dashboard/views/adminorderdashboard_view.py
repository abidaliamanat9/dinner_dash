from django.shortcuts import render
from django.views import View
from dashboard.models.order_model import Order
from dashboard.mixin import AdminRequiredMixin


class AdminOrderDashboardView(AdminRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.all()
        order_status_counts = {
            "ordered": Order.objects.filter(status="ORDERED").count(),
            "paid": Order.objects.filter(status="PAID").count(),
            "cancelled": Order.objects.filter(status="CANCELLED").count(),
            "completed": Order.objects.filter(status="COMPLETED").count(),
        }

        return render(
            request,
            "dashboard/ordersdashboard.html",
            {
                "orders": orders,
                "order_status_counts": order_status_counts,
            },
        )
