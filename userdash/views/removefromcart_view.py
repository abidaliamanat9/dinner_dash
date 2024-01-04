from django.shortcuts import redirect
from django.views import View
from dashboard.models.cartitem_model import CartItem


class RemoveFromCartView(View):
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
