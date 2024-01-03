from django.contrib.auth.forms import UserCreationForm
from django.forms import ValidationError
from .models import User
import re


def is_valid_email(email):
    email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    return bool(re.match(email_regex, email))


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "display_name",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not is_valid_email(email):
            raise ValidationError("Enter a valid email address")

        return email

    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"]
        if len(first_name) > 50:
            raise ValidationError("First name should be less than 50 characters.")

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]
        if len(last_name) > 50:
            raise ValidationError("Last name should be less than 50 characters.")

        return last_name

    def clean_display_name(self):
        display_name = self.cleaned_data["display_name"]
        if display_name is not None:
            if len(display_name) < 2 or len(display_name) > 32:
                raise ValidationError(
                    "Display name should be between 2 and 32 characters"
                )
