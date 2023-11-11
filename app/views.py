from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import *
import json
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.orderproduct_set.all()
        cartItems = order.get_cart_items
    else:
        items=[]
        order={'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
    Products = Product.objects.all()
    context={'Products': Products, 'CartItems': cartItems}
    return render(request,'app/home.html',context)
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.orderproduct_set.all()
        cartItems = order.get_cart_items
    else:
        items=[]
        order={'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
    context={'items':items, 'order': order,'CartItems': cartItems}
    return render(request,'app/cart.html', context)
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.orderproduct_set.all()
        cartItems = order.get_cart_items
    else:
        items=[]
        order={'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
    context={'items':items, 'order': order, 'CartItems': cartItems}
    return render(request,'app/checkout.html', context)

def product_detail(request, product_id):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.orderproduct_set.all()
        cartItems = order.get_cart_items
    else:
        items=[]
        order={'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
    product = get_object_or_404(Product, pk=product_id)
    context={'product': product, 'CartItems': cartItems}
    return render(request, 'app/infor_products.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productID']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderProduct, created = OrderProduct.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderProduct.quantity += 1
    elif action == 'remove':
        orderProduct.quantity -= 1
    if orderProduct.quantity <= 0:
        orderProduct.delete()
    else:
        orderProduct.save()


    return JsonResponse('added', safe=False)
