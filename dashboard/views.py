from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView
from dashboard.models import Category, Item, Order, CartItem, Resturant
from dashboard.mixin import AdminRequiredMixin
from django.contrib import messages
from dashboard.forms import CategoryForm, ResturantForm, ItemForm


class ItemCreateView(AdminRequiredMixin, CreateView):
    model = Item
    template_name = "dashboard/item_create.html"
    form_class = ItemForm
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        messages.success(self.request, "Item created successfully.")
        return super().form_valid(form)


class ItemUpdateView(AdminRequiredMixin, UpdateView):
    model = Item
    template_name = "dashboard/item_update.html"
    form_class = ItemForm
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        messages.success(self.request, "Item Updated successfully.")
        return super().form_valid(form)


class ResturantCreateView(AdminRequiredMixin, CreateView):
    model = Resturant
    template_name = "dashboard/resturant_create.html"
    form_class = ResturantForm
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        messages.success(self.request, "Resturant created successfully.")
        return super().form_valid(form)


class ResturantUpdateView(AdminRequiredMixin, UpdateView):
    model = Resturant
    template_name = "dashboard/resturant_update.html"
    form_class = ResturantForm
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        messages.success(self.request, "Resturant updated successfully.")
        return super().form_valid(form)


class CategoryCreateView(AdminRequiredMixin, CreateView):
    model = Category
    template_name = "dashboard/category_create.html"
    form_class = CategoryForm
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        messages.success(self.request, "Category created successfully.")
        return super().form_valid(form)


class CategoryUpdateView(AdminRequiredMixin, UpdateView):
    model = Category
    template_name = "dashboard/category_update.html"
    form_class = CategoryForm
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        messages.success(self.request, "Category updated successfully.")
        return super().form_valid(form)


class Dashboard(AdminRequiredMixin, View):
    def get(self, request):
        resturants = Resturant.objects.all()
        categories = Category.objects.all()
        items = Item.objects.all()

        return render(
            request,
            "dashboard/dashboard.html",
            {"resturants": resturants, "categories": categories, "items": items},
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


def orderOperation(request, order_id, status):
    try:
        order = Order.objects.get(pk=order_id)
        order.status = status
        order.save()
        messages.success(request, f"Order with {order_id} is {status}")
    except:
        messages.warning(request, "Order not exists")


class OrderCancelView(AdminRequiredMixin, View):
    def get(self, request, order_id):
        orderOperation(request=request, order_id=order_id, status="CANCELLED")
        return redirect("ordersdashboard")


class OrderPaidView(AdminRequiredMixin, View):
    def get(self, request, order_id):
        orderOperation(request=request, order_id=order_id, status="PAID")
        return redirect("ordersdashboard")


class OrderCompletedView(AdminRequiredMixin, View):
    def get(self, request, order_id):
        orderOperation(request=request, order_id=order_id, status="COMPLETED")
        return redirect("ordersdashboard")


def orderfilter(request, status):
    orders = Order.objects.filter(status=status)
    status = status
    return render(
        request, "dashboard/filterorders.html", {"orders": orders, "status": status}
    )


class OrderedView(AdminRequiredMixin, View):
    def get(self, request):
        orderfilter(request=request, status="ORDERED")


class PaidView(AdminRequiredMixin, View):
    def get(self, request):
        orderfilter(request=request, status="PAID")


class CanceledView(AdminRequiredMixin, View):
    def get(self, request):
        orderfilter(request=request, status="CANCELLED")


class CompletedView(AdminRequiredMixin, View):
    def get(self, request):
        orderfilter(request=request, status="COMPLETED")
