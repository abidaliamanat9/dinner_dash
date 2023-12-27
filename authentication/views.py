from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from .forms import SignUpForm
from dashboard.models import CartItem
from django.db import transaction
import pdb

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('login')
            # login(request, user)
            # return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'authentication/signup.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'registration/login.html' 

    def form_valid(self, form):
        response = super().form_valid(form)
        cart = self.request.session.get('cart', [])
        pdb.set_trace()
        if self.request.user.is_authenticated and not self.request.user.is_staff:
            with transaction.atomic():
                for item_data in cart:
                    quantity = item_data.get('quantity')
                    item_id = item_data.get('id')
                    CartItem.objects.create(quantity=quantity, item_id=item_id, user=self.request.user)
                self.request.session.pop('cart', None)
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)

        return response

    def get_success_url(self):
        if self.request.user.is_staff:
           return 'http://127.0.0.1:8000/dashboard/' 
        else:
            return 'http://127.0.0.1:8000/userdash/'  

class CustomLogoutView(LogoutView):
    next_page = 'home'  