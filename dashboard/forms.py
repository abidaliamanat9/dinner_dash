from django import forms
from dashboard.models import Category, Resturant, Item


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


class ItemForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    class Meta:
        model = Item
        fields = ["title", "description", "price", "photo", "category", "resturant"]

    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) < 5 or len(title) > 50:
            raise forms.ValidationError(
                "Enter Item name between 5 to 50 characters"
            )
        return title

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price
