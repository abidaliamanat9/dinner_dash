from django.urls import path
from userdash import views

urlpatterns = [
    path("", views.UserHomeView.as_view(), name="userhome"),
    path("popular-item/", views.PopularItemView.as_view(), name="popularitem"),
    path(
        "category-items/<int:cg_id>/",
        views.CategoryItemsView.as_view(),
        name="categoryitems",
    ),
    path(
        "resturant-items/<int:rest_id>/",
        views.ResturantItemsView.as_view(),
        name="resturantitems",
    ),
    path("detail/<int:pk>/", views.ItemDetailView.as_view(), name="item_detail"),
    path("add-to-cart/<int:item_id>/", views.AddToCartView.as_view(), name="add_to_cart"),
    path("my-cart/", views.MyCartView.as_view(), name="mycart"),
    path("del-cart/", views.ClearCartView.as_view(), name="clearcart"),
    path(
        "remove-from-cart/<int:item_id>/", views.RemoveFromCartView.as_view(), name="rmfromcart"
    ),
    path("checkout/", views.CheckOutView.as_view(), name="checkout"),
    path("my-orders/", views.MyOrdersView.as_view(), name="myorders"),
    path(
        "my-order-detail/<int:order_id>/",
        views.OrderDetailView.as_view(),
        name="myorder_detail",
    ),
    path(
        "modify-quantity/<int:item_id>/",
        views.ModifyQuantityView.as_view(),
        name="modifyquantity",
    ),
]
