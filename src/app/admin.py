from django.contrib import admin
from .models import *
from .forms import ProductAdminForm
from django.utils.html import format_html

class ProductModelAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('image_preview', 'name', 'quantity', 'price',) 

    def image_preview(self, obj):
        return format_html('<img src="{0}" width="auto" height="150px">'.format(obj.image.url))
    


admin.site.register(Product, ProductModelAdmin)
# Register your models here.
admin.site.register(PurchaseItem)
admin.site.register(CustomerPurchase)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Profile)