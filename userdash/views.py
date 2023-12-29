from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import DetailView, ListView
from django.http import HttpResponse
from dashboard.models import Category, Item, CartItem, Order
from django.contrib.auth.mixins import LoginRequiredMixin
import pdb


class UserHomeView(View):
    def get(self, request):
        categories = Category.objects.all()
        items = Item.objects.filter(retired=False)

        return render(
            request,
            "userdash/userhome.html",
            {"categories": categories, "items": items},
        )


class CategoryItemsView(View):
    def get(self, request, cg_id):
        categories = Category.objects.all()
        items = Item.objects.filter(category__id=cg_id)
        return render(
            request,
            "userdash/userhome.html",
            {"categories": categories, "items": items},
        )


class ItemDetail(DetailView):
    model = Item
    template_name = "userdash/item_detail.html"
    context_object_name = "item"


class AddToCart(View):
    def get(self, request, item_id):
        try:
            item = Item.objects.get(pk=item_id)
        except ObjectDoesNotExist:
            return HttpResponse("Item not found", status=404)
        if request.user.is_authenticated and not request.user.is_staff:
            try:
                cartitem = CartItem.objects.get(item=item, order=None)
                cartitem.quantity += 1
                cartitem.stprice = cartitem.quantity * item.price
                cartitem.save()
            except:
                CartItem.objects.create(
                    item=item,
                    quantity=1,
                    stprice=item.price,
                    order=None,
                    user=request.user,
                )
        else:
            cart = request.session.get("cart", [])

            for cart_item in cart:
                if cart_item["id"] == item.id:
                    cart_item["quantity"] += 1
                    cart_item["stprice"] = cart_item["quantity"] * cart_item["price"]
                    request.session.save()
            cart.append(
                {
                    "id": item.id,
                    "name": item.title,
                    "quantity": 1,
                    "price": float(item.price),
                    "stprice": float(item.price),
                }
            )
            request.session["cart"] = cart
            request.session.save()

        return redirect("userhome")


class MyCart(View):
    def get(self, request):
        if request.user.is_authenticated and not request.user.is_staff:
            cart = CartItem.objects.filter(user=request.user, order=None)
            total_items = sum(item.quantity for item in cart)
            total_price = sum(item.stprice for item in cart)
        else:
            cart = request.session.get("cart", [])
            total_items = sum(item["quantity"] for item in cart)
            total_price = sum(item["stprice"] for item in cart)
        return render(
            request,
            "userdash/mycart.html",
            {"cart": cart, "total_items": total_items, "total_price": total_price},
        )


class ClearCart(View):
    def get(self, request):
        if request.user.is_authenticated and not request.user.is_staff:
            items = CartItem.objects.filter(user=request.user, order=None)
            items.delete()
        else:
            request.session.pop("cart", None)
        return redirect("userhome")


class RemoveFromCart(View):
    def get(self, request, item_id):
        if request.user.is_authenticated and not request.user.is_staff:
            item = CartItem.objects.filter(id=item_id, order_id=None)
            item.delete()
        else:
            cart = request.session.get("cart", [])
            index_to_remove = None
            for i, item in enumerate(cart):
                if item["id"] == item_id:
                    index_to_remove = i
                    break
            if index_to_remove is not None:
                cart.pop(index_to_remove)
                request.session["cart"] = cart
                request.session.save()
        return redirect("mycart")


class CheckOutView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")

    def get(self, request):
        order = Order.objects.create(user=request.user)
        cartitems = CartItem.objects.filter(user=request.user, order=None).update(
            order=order
        )
        return redirect("userhome")


class MyOrdersView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("login")

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        return render(request, "userdash/myorders.html", {"orders": orders})


class OrderDetailView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("login")

    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        cartitems = CartItem.objects.filter(user=request.user, order=order)
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
