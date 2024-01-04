from django.shortcuts import redirect
from django.views import View
from dashboard.models.cartitem_model import CartItem


class ClearCartView(View):
    def get(self, request):
        if request.user.is_authenticated and not request.user.is_staff:
            items = CartItem.objects.filter(user=request.user, order=None)
            items.delete()
        else:
            request.session.pop("cart", None)
            request.session.pop("resturant_id", None)
        return redirect("userhome")
