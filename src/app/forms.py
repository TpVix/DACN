from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Product, CustomerPurchase


class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Product
        fields = '__all__'
        


class CheckoutForm(forms.Form):
    customer_name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=200)
    phone_number = forms.CharField(max_length=20)
