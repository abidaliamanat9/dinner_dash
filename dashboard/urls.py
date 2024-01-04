from django.urls import path
from dashboard import views

urlpatterns = [
    path("item-create/", views.ItemCreateView.as_view(), name="item_create"),
    path("item-update/<int:pk>/", views.ItemUpdateView.as_view(), name="item_update"),
    path(
        "category-create/", views.CategoryCreateView.as_view(), name="category_create"
    ),
    path(
        "category-update/<int:pk>/",
        views.CategoryUpdateView.as_view(),
        name="category_update",
    ),
    path(
        "resturant-create/",
        views.ResturantCreateView.as_view(),
        name="resturant_create",
    ),
    path(
        "resturant-update/<int:pk>/",
        views.ResturantUpdateView.as_view(),
        name="resturant_update",
    ),
    path("admin-dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path(
        "orders-dashboard/",
        views.AdminOrderDashboardView.as_view(),
        name="ordersdashboard",
    ),
    path(
        "order-detail/<int:order_id>/",
        views.OrderDetailView.as_view(),
        name="orderdetail",
    ),
    path(
        "modify-order/<int:order_id>/",
        views.ModifyOrderView.as_view(),
        name="modifyorder",
    ),
    path(
        "filter-order/",
        views.FilterOrderView.as_view(),
        name="filterorder",
    ),
]
