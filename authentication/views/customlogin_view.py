from django.contrib.auth.views import LoginView
from dashboard.models.cartitem_model import CartItem
from django.urls import reverse_lazy
from django.contrib import messages


class CustomLoginView(LoginView):
    template_name = "registration/login.html"

    def form_invalid(self, form):
        response = super().form_invalid(form)
        return response

    def form_valid(self, form):
        response = super().form_valid(form)
        cart = self.request.session.get("cart", [])
        if self.request.user.is_authenticated and not self.request.user.is_staff:
            for item_data in cart:
                quantity = item_data.get("quantity")
                item_id = item_data.get("id")
                price = item_data.get("price")
                CartItem.objects.create(
                    quantity=quantity,
                    item_id=item_id,
                    price=price,
                    user=self.request.user,
                )
            self.request.session.pop("cart", None)
        return response

    def get_success_url(self):
        messages.success(self.request, "User Log In Successfuly")
        if self.request.user.is_staff:
            return reverse_lazy("dashboard")
        else:
            return reverse_lazy("userhome")
