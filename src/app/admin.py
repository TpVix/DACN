from django.contrib import admin
from .models import *
from .forms import ProductAdminForm

class ProductModelAdmin(admin.ModelAdmin):
    form = ProductAdminForm

admin.site.register(Product, ProductModelAdmin)
# Register your models here.
admin.site.register(PurchaseItem)
admin.site.register(CustomerPurchase)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderProduct)


