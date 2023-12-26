from django.urls import path
from .views import home,ItemDetail

urlpatterns = [
    path('',home, name='home'),
    path('detail/<int:pk>/',ItemDetail.as_view(), name = 'item_detail'),
]