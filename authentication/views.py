from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from .forms import SignUpForm
from dashboard.models import CartItem
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages


class SignupView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, "authentication/signup.html", {"form": form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            messages.success(
                request, "You account is created successfuly, please login to continue"
            )
            return redirect("login")
        else:
            return render(request, "authentication/signup.html", {"form": form})


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
                CartItem.objects.create(
                    quantity=quantity,
                    item_id=item_id,
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


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("userhome")
