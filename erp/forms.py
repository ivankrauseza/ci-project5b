from django import forms
from shop.models import Product, Media, SalesOrder


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'sku', 'name', 'blurb', 'stock', 'price', 'brand',
            'collection', 'type'
        ]
        labels = {
            'sku': 'SKU',
            'name': 'Product Name',
            'blurb': 'Blurb',
            'stock': 'Stock Quantity',
            'price': 'Price',
            'brand': 'Brand',
            'collection': 'Product Collection',
            'type': 'Product Type',
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['file']


class SalesOrderStatusForm(forms.ModelForm):
    class Meta:
        model = SalesOrder
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }