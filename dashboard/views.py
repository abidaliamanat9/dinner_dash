from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from .models import Category,Item
from .mixin import AdminRequiredMixin

class ItemCreateView(AdminRequiredMixin,CreateView):
    model = Item
    template_name = 'dashboard/item_create.html'
    fields = ['title', 'description', 'price', 'photo', 'category']  
    success_url = reverse_lazy('dashboard') 
    # login_url = reverse('accounts/login')

class ItemUpdateView(AdminRequiredMixin,UpdateView):
    model = Item
    template_name = 'dashboard/item_update.html'
    fields = ['title', 'description', 'price', 'photo', 'category'] 
    success_url = reverse_lazy('dashboard')  

class ItemListView(ListView):
    model = Item
    template_name = 'item_list.html'
    fields = ['title', 'description', 'price', 'photo']
    context_object_name = 'items'
    

class CategoryCreateView(AdminRequiredMixin,CreateView):
    model = Category
    template_name = 'dashboard/category_create.html'
    fields = ['name'] 
    success_url = reverse_lazy('dashboard') 

class CategoryUpdateView(AdminRequiredMixin,UpdateView):
    model = Category
    template_name = 'dashboard/category_update.html'
    fields = ['name'] 
    success_url = reverse_lazy('dashboard') 

def dashboard(request):
    return render(request,'dashboard/dashboard.html')

