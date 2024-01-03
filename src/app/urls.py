from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('home', views.home, name="home"),
    path('cart', views.cart, name="cart"),
    path('checkout/', views.checkout, name='checkout'),
    path('product_detail/<int:id>/', views.product_detail, name='product_detail'),
    path('update_item/', views.updateItem, name="update_item"),
    path('register/', views.register, name="register"),
    path('login/', views.loginuser, name="login"),
    path('logout/', views.logoutuser, name="logout"),
    path('search/', views.search, name="search"),
    path('category/', views.category, name="category"),
    path('aboutme/', views.aboutme, name="aboutme"),
    path('change_password/', views.PasswordchangeView.as_view(template_name = "app/password_change.html"), name="change_password"),
    path('password_success/', views.password_success, name="password_success"),
    path('editprofile/', views.UpdateUserView.as_view(), name="editprofile"),
    path('token_send/', views.token_send, name="token_send"),
    path('success/', views.success, name="success"),
    path('verify/<auth_token>' , views.verify , name="verify"),

]