from django.urls import path
from dashboard import views

urlpatterns = [
    path("item/create/", views.ItemCreateView.as_view(), name="item_create"),
    path("item/update/<int:pk>/", views.ItemUpdateView.as_view(), name="item_update"),
    path(
        "category/create/", views.CategoryCreateView.as_view(), name="category_create"
    ),
    path(
        "category/update/<int:pk>/",
        views.CategoryUpdateView.as_view(),
        name="category_update",
    ),
    path(
        "resturant/create/", views.ResturantCreateView.as_view(), name="resturant_create"
    ),
    path(
        "resturant/update/<int:pk>/",
        views.ResturantUpdateView.as_view(),
        name="resturant_update",
    ),
    path("adminhome/", views.Dashboard.as_view(), name="dashboard"),
    path(
        "ordersdashboard/",
        views.AdminOrderDashboardView.as_view(),
        name="ordersdashboard",
    ),
    path(
        "orderdetail/<int:order_id>/",
        views.OrderDetailView.as_view(),
        name="orderdetail",
    ),
    path(
        "cancelorder/<int:order_id>/",
        views.OrderCancelView.as_view(),
        name="cancelorder",
    ),
    path(
        "paidorder/<int:order_id>/",
        views.OrderPaidView.as_view(),
        name="paidorder",
    ),
    path(
        "completedorder/<int:order_id>/",
        views.OrderCompletedView.as_view(),
        name="completedorder",
    ),
    path(
        "orderedorderfilter/",
        views.OrderedView.as_view(),
        name="orderedorderfilter",
    ),
    path(
        "paidorderfilter/",
        views.PaidView.as_view(),
        name="paidorderfilter",
    ),
    path(
        "canceledorderfilter/",
        views.CanceledView.as_view(),
        name="canceledorderfilter",
    ),
    path(
        "completedorderfilter/",
        views.CompletedView.as_view(),
        name="completedorderfilter",
    ),
]
