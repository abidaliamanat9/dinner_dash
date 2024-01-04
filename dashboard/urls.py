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
    path("admin-dashboard/", views.Dashboard.as_view(), name="dashboard"),
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
        "cancel-order/<int:order_id>/",
        views.OrderCancelView.as_view(),
        name="cancelorder",
    ),
    path(
        "paid-order/<int:order_id>/",
        views.OrderPaidView.as_view(),
        name="paidorder",
    ),
    path(
        "completed-order/<int:order_id>/",
        views.OrderCompletedView.as_view(),
        name="completedorder",
    ),
    path(
        "ordered-order-filter/",
        views.OrderedView.as_view(),
        name="orderedorderfilter",
    ),
    path(
        "paid-order-filter/",
        views.PaidView.as_view(),
        name="paidorderfilter",
    ),
    path(
        "canceled-order-filter/",
        views.CanceledView.as_view(),
        name="canceledorderfilter",
    ),
    path(
        "completed-order-filter/",
        views.CompletedView.as_view(),
        name="completedorderfilter",
    ),
]
