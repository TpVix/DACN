from django.utils import timezone
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User 
from ckeditor.fields import RichTextField
from django.shortcuts import get_object_or_404
from django import forms
from django.contrib.auth.admin import UserAdmin

from userauths.models import CustomUser
# change forms register django

class Category(models.Model):
    name = models.CharField(max_length=200, null=True)
    image = models.ImageField(null=True,blank=True)
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_categories', null=True, blank=True)
    is_sub = models.BooleanField(default=True)
    slug = models.SlugField(max_length=200, null=True)
    def __str__(self):
        return self.name
    @property
    def ImgURL (self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
class Product(models.Model):
    name = models.CharField(max_length=200, null=True, blank=False)
    quantity = models.IntegerField(default=0, null=True, blank=False)
    description = RichTextField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    category = models.ManyToManyField(Category, related_name='Categories')
    image = models.ImageField(null=True,blank=True)
   
    def __str__(self):
        return self.name
    @property
    def ImgURL (self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=False)
    order_date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True, blank=False)

    def __str__(self):
        return str(self.id)
    @property
    def get_cart_items(self):
        orderproduct = self.orderproduct_set.all()
        total = sum([item.quantity for item in orderproduct])
        return total
    @property
    def get_cart_total(self):
        orderproduct = self.orderproduct_set.all()
        total = sum([item.get_total for item in orderproduct])
        return total
    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=False)
    quantity = models.IntegerField(default=0, null=True, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class CustomerPurchase(models.Model):
    customer_name = models.CharField(max_length=100, null=True, blank=False)
    address = models.CharField(max_length=200, null=True, blank=False)
    email = models.CharField(max_length=200, null=True, blank=False)
    phone_number = models.CharField(max_length=20, null=True, blank=False)
    products = models.ManyToManyField(Product, through='PurchaseItem')
    purchase_date = models.DateTimeField(default=timezone.now)
    total_quantity = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        local_purchase_date = timezone.localtime(self.purchase_date)
        return f"{self.customer_name} Mua hàng vào lúc {local_purchase_date.strftime('%Y-%m-%d %H:%M:%S')}"


class PurchaseItem(models.Model):
    customer_purchase = models.ForeignKey(CustomerPurchase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Hoặc bất kỳ trường nào khác bạn muốn lưu thông tin sản phẩm
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Các trường thông tin khác nếu cần

    def __str__(self):
        return f"Khách hàng: {self.customer_purchase}-Tên sản phẩm: {self.product.name} - Số lượng: {self.quantity}"
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Tính toán tổng giá và tổng số lượng của tất cả PurchaseItem liên quan
        purchase = self.customer_purchase
        purchase_items = PurchaseItem.objects.filter(customer_purchase=purchase)
        total_quantity = purchase_items.aggregate(models.Sum('quantity'))['quantity__sum'] or 0
        total_price = sum(item.product.price * item.quantity for item in purchase_items)
        
        # Cập nhật giá trị tổng giá và tổng số lượng vào CustomerPurchase
        purchase.total_quantity = total_quantity
        purchase.total_price = total_price
        purchase.save()


class Profile (models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=250)
    is_verified = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username