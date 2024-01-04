from django.shortcuts import redirect
from django.views import View
from dashboard.models.item_model import Item
from dashboard.models.cartitem_model import CartItem
from django.contrib import messages


class ModifyQuantityView(View):
    def get(self, request, item_id):
        action = request.GET.get("action", "increment")
        if request.user.is_authenticated and not request.user.is_staff:
            try:
                cartitem = CartItem.objects.get(
                    pk=item_id, order=None, user=request.user
                )
                if action == "increment":
                    cartitem.quantity += 1
                    messages.success(request, "Quantity Increase by 1")
                else:
                    if cartitem.quantity < 2:
                        cartitem.quantity = 1
                        messages.warning(request, "Cannot Decrease Quantity")
                    else:
                        cartitem.quantity -= 1
                        messages.success(request, "Quantity Decrease by 1")
                cartitem.save()

            except (Item.DoesNotExist, CartItem.DoesNotExist):
                messages.warning(request, "Item not exists for this operation")
        else:
            cart = request.session.get("cart", [])
            for cart_item in cart:
                if cart_item["id"] == item_id:
                    if action == "increment":
                        cart_item["quantity"] += 1
                        messages.success(request, "Quantity Increase by 1")
                    else:
                        if cart_item["quantity"] < 2:
                            cart_item["quantity"] = 1
                            messages.warning(request, "Cannot Decrease Quantity")
                        else:
                            cart_item["quantity"] -= 1
                            messages.success(request, "Quantity Decrease by 1")
                    cart_item["stprice"] = cart_item["quantity"] * cart_item["price"]
                    request.session.save()
            request.session["cart"] = cart
            request.session.save()
        return redirect("mycart")
