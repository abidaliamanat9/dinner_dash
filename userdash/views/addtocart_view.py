from django.shortcuts import redirect
from django.views import View
from dashboard.models.item_model import Item
from dashboard.models.cartitem_model import CartItem
from django.contrib import messages


class AddToCartView(View):
    def get(self, request, item_id):
        try:
            item = Item.objects.get(pk=item_id)
        except Item.DoesNotExist:
            messages.warning(request, "This Item is not existing")
            return redirect("userhome")
        resturant = item.resturant
        if request.user.is_authenticated and not request.user.is_staff:
            try:
                cartitem = CartItem.objects.get(
                    item=item, order=None, user=request.user
                )
                cartitem.quantity += 1
                cartitem.save()
                messages.success(
                    request, "Item already in your cart! quantity is increased by 1"
                )
            except CartItem.DoesNotExist:
                cartitems = CartItem.objects.filter(
                    order=None, user=request.user
                ).first()
                if cartitems and cartitems.item.resturant.id != resturant.id:
                    messages.warning(
                        request, "You can only add items from one restaurant at a time."
                    )
                    return redirect("userhome")
                CartItem.objects.create(
                    item=item,
                    quantity=1,
                    price=item.price,
                    order=None,
                    user=request.user,
                )
                messages.success(request, "Item was added to cart successfuly")
            finally:
                return redirect("userhome")
        else:
            current_resturant_id = request.session.get("resturant_id")
            if current_resturant_id and current_resturant_id != resturant.id:
                messages.warning(
                    request, "You can only add items from one restaurant at a time."
                )
                return redirect("userhome")
            cart = request.session.get("cart", [])

            for cart_item in cart:
                if cart_item["id"] == item.id:
                    cart_item["quantity"] += 1
                    cart_item["stprice"] = cart_item["quantity"] * cart_item["price"]
                    request.session.save()
                    messages.success(
                        request, "Item already in your cart! quantity is increased by 1"
                    )
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
            request.session["resturant_id"] = resturant.id
            request.session.save()
            messages.success(request, "Item was added to cart successfuly")
            return redirect("userhome")
