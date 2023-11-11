from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('cart', views.cart, name="cart"),
    path('checkout', views.checkout, name="checkout"),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('update_item/', views.updateItem, name="update_item"),
]