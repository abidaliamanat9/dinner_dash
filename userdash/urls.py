from django.urls import path
from .views import home,mycart,delcart,removeFromCart,ItemDetail,AddToCart

urlpatterns = [
    path('',home, name='home'),
    path('detail/<int:pk>/',ItemDetail.as_view(), name = 'item_detail'),
    path('add_to_cart/<int:item_id>/',AddToCart.as_view(), name = 'add_to_cart'),
    path('mycart/', mycart, name='mycart'),
    path('delcart/', delcart, name='delcart'),
    path('rmfromcart/<int:item_id>/', removeFromCart, name='rmfromcart'),
]