from django import forms
from dashboard.models.category_model import Category
from dashboard.models.item_model import Item

class ItemForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.SelectMultiple,
        required=True,
    )

    class Meta:
        model = Item
        fields = ["title", "description", "price", "photo", "category", "resturant"]

    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) < 5 or len(title) > 50:
            raise forms.ValidationError("Enter Item name between 5 to 50 characters")
        return title

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price
