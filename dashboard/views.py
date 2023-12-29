from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView
from dashboard.models import Category, Item, Order, CartItem
from dashboard.mixin import AdminRequiredMixin
from django.utils import timezone


class ItemCreateView(AdminRequiredMixin, CreateView):
    model = Item
    template_name = "dashboard/item_create.html"
    fields = ["title", "description", "price", "photo", "category"]
    success_url = reverse_lazy("dashboard")
    # login_url = reverse('accounts/login')


class ItemUpdateView(AdminRequiredMixin, UpdateView):
    model = Item
    template_name = "dashboard/item_update.html"
    fields = ["title", "description", "price", "photo", "retired", "category"]
    success_url = reverse_lazy("dashboard")


class CategoryCreateView(AdminRequiredMixin, CreateView):
    model = Category
    template_name = "dashboard/category_create.html"
    fields = ["name"]
    success_url = reverse_lazy("dashboard")


class CategoryUpdateView(AdminRequiredMixin, UpdateView):
    model = Category
    template_name = "dashboard/category_update.html"
    fields = ["name"]
    success_url = reverse_lazy("dashboard")


class Dashboard(View):
    def get(self, request):
        categories = Category.objects.all()
        items = Item.objects.all()

        return render(
            request,
            "dashboard/dashboard.html",
            {"categories": categories, "items": items},
        )


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


class OrderDetailView(AdminRequiredMixin, View):
    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        cartitems = CartItem.objects.filter(user=order.user, order=order)
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


class OrderCancelView(AdminRequiredMixin, View):
    def get(self, request, order_id):
        order = Order.objects.get(pk=order_id)
        order.status = "CANCELLED"
        order.status_changed_at = timezone.now()
        order.save()
        return redirect("ordersdashboard")


class OrderPaidView(AdminRequiredMixin, View):
    def get(self, request, order_id):
        order = Order.objects.get(pk=order_id)
        order.status = "PAID"
        order.status_changed_at = timezone.now()
        order.save()
        return redirect("ordersdashboard")


class OrderCompletedView(AdminRequiredMixin, View):
    def get(self, request, order_id):
        order = Order.objects.get(pk=order_id)
        order.status = "COMPLETED"
        order.status_changed_at = timezone.now()
        order.save()
        return redirect("ordersdashboard")


class OrderedView(AdminRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.filter(status="ORDERED")
        status = "Ordered"
        return render(
            request, "dashboard/filterorders.html", {"orders": orders, "status": status}
        )


class PaidView(AdminRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.filter(status="PAID")
        status = "Paid"
        return render(
            request, "dashboard/filterorders.html", {"orders": orders, "status": status}
        )


class CanceledView(AdminRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.filter(status="CANCELED")
        status = "Canceled"
        return render(
            request, "dashboard/filterorders.html", {"orders": orders, "status": status}
        )


class CompletedView(AdminRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.filter(status="COMPLETED")
        status = "Completed"
        return render(
            request, "dashboard/filterorders.html", {"orders": orders, "status": status}
        )
