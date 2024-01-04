from django.urls import path
from authentication.views import CustomLoginView, CustomLogoutView, SignupView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
]
