from django.urls import path
from dashboard import views

urlpatterns = [
    path("item/create/", views.ItemCreateView.as_view(), name="item_create"),
    path("item/update/<int:pk>/", views.ItemUpdateView.as_view(), name="item_update"),
    path("item/delete/<int:pk>/", views.ItemDeleteView.as_view(), name="item_delete"),
    path(
        "category/create/", views.CategoryCreateView.as_view(), name="category_create"
    ),
    path(
        "category/update/<int:pk>/",
        views.CategoryUpdateView.as_view(),
        name="category_update",
    ),
    path(
        "category/delete/<int:pk>/",
        views.CategoryDeleteView.as_view(),
        name="category_delete",
    ),
    path("adminhome/", views.Dashboard.as_view(), name="dashboard"),
]
