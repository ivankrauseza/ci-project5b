from django import forms
from .models import Transaction


class AddToBasketForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)

        # Set max_value dynamically based on available stock
        if self.product:
            max_stock = self.product.stock if self.product.stock > 0 else 1
            self.fields['quantity'] = forms.IntegerField(
                min_value=1,
                max_value=max_stock,
                label='Quantity',
                widget=forms.NumberInput(attrs={'class': 'quantity', 'placeholder': '0'})
            )

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is None:
            raise forms.ValidationError("Please enter a quantity.")
        if self.product and quantity > self.product.stock:
            raise forms.ValidationError("Insufficient stock.")
        return quantity
