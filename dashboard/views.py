from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from dashboard.models import Category, Item
from dashboard.mixin import AdminRequiredMixin


class ItemCreateView(AdminRequiredMixin, CreateView):
    model = Item
    template_name = "dashboard/item_create.html"
    fields = ["title", "description", "price", "photo", "category"]
    success_url = reverse_lazy("dashboard")
    # login_url = reverse('accounts/login')


class ItemUpdateView(AdminRequiredMixin, UpdateView):
    model = Item
    template_name = "dashboard/item_update.html"
    fields = ["title", "description", "price", "photo", "category"]
    success_url = reverse_lazy("dashboard")


class ItemDeleteView(AdminRequiredMixin, DeleteView):
    model = Item
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


class CategoryDeleteView(AdminRequiredMixin, DeleteView):
    model = Category
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
