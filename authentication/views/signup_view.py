from django.shortcuts import render, redirect
from authentication.forms import SignUpForm
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
