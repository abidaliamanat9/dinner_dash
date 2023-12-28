from django.shortcuts import redirect, render
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import DetailView
from django.http import HttpResponse
from dashboard.models import Category, Item


class UserHomeView(View):
    def get(self, request):
        categories = Category.objects.all()
        items = Item.objects.all()

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

        cart = request.session.get("cart", [])

        for cart_item in cart:
            if cart_item["id"] == item.id:
                cart_item["quantity"] += 1
                cart_item["stprice"] = cart_item["quantity"] * cart_item["price"]
                request.session.save()
                return redirect("userhome")
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
        cart = request.session.get("cart", [])

        total_items = sum(item["quantity"] for item in cart)
        total_price = sum(item["quantity"] * item["price"] for item in cart)
        return render(
            request,
            "userdash/mycart.html",
            {"cart": cart, "total_items": total_items, "total_price": total_price},
        )


class ClearCart(View):
    def get(self, request):
        request.session.pop("cart", None)
        return redirect("userhome")


class RemoveFromCart(View):
    def get(self, request, item_id):
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
