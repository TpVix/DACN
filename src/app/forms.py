from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Product, CustomerPurchase
from userauths.models import CustomUser
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation


class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget) 
    
    class Meta:
        model = Product
        fields = '__all__'
        
class CheckoutForm(forms.Form):
    customer_name = forms.CharField(max_length=100)
    email = forms.CharField(max_length=200)
    address = forms.CharField(max_length=200)
    phone_number = forms.CharField(max_length=20)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'address', 'phone_number']

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mật khẩu cũ'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mật khẩu mới'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Xác nhận'}))
    class Meta:
        model = CustomUser
        fields = ['old_password', 'new_password1', 'new_password2']


class EditUserForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Địa chỉ'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Số điện thoại'}))
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name','email','address', 'phone_number']