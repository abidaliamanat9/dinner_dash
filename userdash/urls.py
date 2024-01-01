from django.urls import path
from userdash.views import (
    RemoveFromCart,
    UserHomeView,
    MyCart,
    ClearCart,
    ItemDetail,
    AddToCart,
    CategoryItemsView,
    CheckOutView,
    MyOrdersView,
    OrderDetailView,
)

urlpatterns = [
    path("", UserHomeView.as_view(), name="userhome"),
    path(
        "categoryitems/<int:cg_id>/", CategoryItemsView.as_view(), name="categoryitems"
    ),
    path("detail/<int:pk>/", ItemDetail.as_view(), name="item_detail"),
    path("add_to_cart/<int:item_id>/", AddToCart.as_view(), name="add_to_cart"),
    path("mycart/", MyCart.as_view(), name="mycart"),
    path("delcart/", ClearCart.as_view(), name="clearcart"),
    path("rmfromcart/<int:item_id>/", RemoveFromCart.as_view(), name="rmfromcart"),
    path("checkout/", CheckOutView.as_view(), name="checkout"),
    path("myorders/", MyOrdersView.as_view(), name="myorders"),
    path("myorderdetail/<int:order_id>/", OrderDetailView.as_view(), name="myorder_detail"),
]
