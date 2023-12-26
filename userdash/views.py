from django.shortcuts import render,get_object_or_404
from django.views.generic import DetailView
from django.http import HttpResponse
from dashboard.models import Category,Item
def home(request):
    categories = Category.objects.all()
    items = Item.objects.all()

    return render(request,'userdash/home.html',{'categories':categories,'items':items})

class ItemDetail(DetailView):
    model = Item
    template_name = 'userdash/item_detail.html'
    context_object_name = 'item'

