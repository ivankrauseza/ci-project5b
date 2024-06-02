from django import forms
from erp.models import Company
from shop.models import Product, Media, SalesOrder


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'name',
            'address',
            'phone',
            'email',
            'website',
            'tax_id',
            'vat_id',
            'reg_id',
            'incorporation_date',
        ]
        labels = {
            'name': 'Company Name',
            'address': 'Registered/Physical Address',
            'phone': 'Phone Number',
            'email': 'Email Address',
            'website': 'Website',
            'tax_id': 'Tax Number',
            'vat_id': 'VAT Number',
            'reg_id': 'Registration Number',
            'incorporation_date': 'Incorporated Date',
        }

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'sku',
            'name',
            'blurb',
            'stock',
            'price',
            'brand',
            'collection',
            'type',
            'seo_keys',
            'seo_desc'
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
            'seo_keys': 'Meta Keywords',
            'seo_desc': 'Meta Description',
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