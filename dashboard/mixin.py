from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            messages.error(
                self.request, "You do not have permission to access this page."
            )
            return super().handle_no_permission()
        else:
            messages.info(
                self.request, "Please log in as an admin to access this page."
            )
            return super().handle_no_permission()
