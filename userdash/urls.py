from django.urls import path
from userdash.views import (
    RemoveFromCart,
    UserHomeView,
    MyCart,
    ClearCart,
    ItemDetail,
    AddToCart,
)

urlpatterns = [
    path("", UserHomeView.as_view(), name="userhome"),
    path("detail/<int:pk>/", ItemDetail.as_view(), name="item_detail"),
    path("add_to_cart/<int:item_id>/", AddToCart.as_view(), name="add_to_cart"),
    path("mycart/", MyCart.as_view(), name="mycart"),
    path("delcart/", ClearCart.as_view(), name="clearcart"),
    path("rmfromcart/<int:item_id>/", RemoveFromCart.as_view(), name="rmfromcart"),
]
