from django import forms
from dashboard.models.category_model import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) < 5 or len(name) > 50:
            raise forms.ValidationError(
                "Enter Category name between 5 to 50 characters"
            )
        return name
