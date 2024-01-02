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
    IncrementQuantityView,
    DecrementQuantityView,
    ResturantItemsView,
    PopularItemView,
)

urlpatterns = [
    path("", UserHomeView.as_view(), name="userhome"),
    path("popularitem/", PopularItemView.as_view(), name="popularitem"),
    path(
        "categoryitems/<int:cg_id>/",
        CategoryItemsView.as_view(),
        name="categoryitems",
    ),
    path(
        "resturantitems/<int:rest_id>/",
        ResturantItemsView.as_view(),
        name="resturantitems",
    ),
    path("detail/<int:pk>/", ItemDetail.as_view(), name="item_detail"),
    path("add_to_cart/<int:item_id>/", AddToCart.as_view(), name="add_to_cart"),
    path("mycart/", MyCart.as_view(), name="mycart"),
    path("delcart/", ClearCart.as_view(), name="clearcart"),
    path("rmfromcart/<int:item_id>/", RemoveFromCart.as_view(), name="rmfromcart"),
    path("checkout/", CheckOutView.as_view(), name="checkout"),
    path("myorders/", MyOrdersView.as_view(), name="myorders"),
    path(
        "myorderdetail/<int:order_id>/",
        OrderDetailView.as_view(),
        name="myorder_detail",
    ),
    path(
        "incrementquantity/<int:item_id>/",
        IncrementQuantityView.as_view(),
        name="incrementquantity",
    ),
    path(
        "decrementquantity/<int:item_id>/",
        DecrementQuantityView.as_view(),
        name="decrementquantity",
    ),
]
