from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# change forms register django
class CreaterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, null=True)
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_categories', null=True, blank=True)
    is_sub = models.BooleanField(default=True)
    slug = models.SlugField(max_length=200, null=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, null=True, blank=False)
    description = models.TextField()
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
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    order_date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

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