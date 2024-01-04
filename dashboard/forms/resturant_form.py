from django import forms
from dashboard.models.resturant_model import Resturant


class ResturantForm(forms.ModelForm):
    class Meta:
        model = Resturant
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) < 5 or len(name) > 50:
            raise forms.ValidationError(
                "Enter Resturant name between 5 to 50 characters"
            )
        return name
