from django import forms
from .models import Transaction, Contact, Support


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


class BasketQuantityForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['quantity']  # Specify only the 'quantity' field

    def clean_quantity(self):
        data = self.cleaned_data['quantity']
        if data < 1:
            raise forms.ValidationError('Quantity must be at least 1.')
        return data


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }


class SupportForm(forms.ModelForm):
    class Meta:
        model = Support
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
