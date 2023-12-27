from django.urls import path
from .views import *

urlpatterns = [
    path('item/create/', ItemCreateView.as_view(), name='item_create'),
    path('item/update/<int:pk>/', ItemUpdateView.as_view(), name='item_update'),
    path('item/delete/<int:pk>/', ItemDeleteView.as_view(), name='item_delete'),
    path('item/list/', ItemListView.as_view(), name='item_list'),
    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    path('',dashboard, name = 'dashboard')
]