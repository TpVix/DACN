from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('cart', views.cart, name="cart"),
    path('checkout/', views.checkout, name='checkout'),
    path('product_detail/<int:id>/', views.product_detail, name='product_detail'),
    path('update_item/', views.updateItem, name="update_item"),
    path('register/', views.register, name="register"),
    path('login/', views.loginuser, name="login"),
    path('logout/', views.logoutuser, name="logout"),
    path('search/', views.search, name="search"),
    path('category/', views.category, name="category"),
]