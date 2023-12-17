from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import *
#Category
def category(request):
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category','')
    if active_category:
        products = Product.objects.filter(category__slug=active_category)
    context={'categories': categories, 'products': products, 'active_category':active_category}
    return render(request,'app/category.html',context)
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.orderproduct_set.all()
        cartItems = order.get_cart_items
    else:
        items=[]
        order={'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
    categories = Category.objects.filter(is_sub = False)
    Products = Product.objects.all()
    context={'categories': categories,'Products': Products, 'CartItems': cartItems}
    return render(request,'app/home.html',context)
def cart(request):
    if not request.user.is_authenticated:
        return redirect('login') 
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.orderproduct_set.all()
        cartItems = order.get_cart_items
    else:
        items=[]
        order={'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
    categories = Category.objects.filter(is_sub = False)
    context={'categories': categories,'items':items, 'order': order,'CartItems': cartItems}
    return render(request,'app/cart.html', context)

def checkout(request):
    order = None
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            customer_name = form.cleaned_data['customer_name']
            address = form.cleaned_data['address']
            phone_number = form.cleaned_data['phone_number']

            if request.user.is_authenticated:
                # Lấy thông tin giỏ hàng của người dùng
                customer = request.user
                order, created = Order.objects.get_or_create(customer=customer, complete=False)
                cart_items = order.orderproduct_set.all()

                # Tạo CustomerPurchase
                purchase = CustomerPurchase.objects.create(
                    customer_name=customer_name,
                    address=address,
                    phone_number=phone_number
                )

                # Lưu thông tin sản phẩm từ giỏ hàng vào CustomerPurchase
                for item in cart_items:
                    PurchaseItem.objects.create(
                        customer_purchase=purchase,
                        product=item.product,
                        quantity=item.quantity
                    )

                # Đánh dấu đơn hàng đã hoàn thành
                order.complete = True
                order.save()

            # Xóa giỏ hàng sau khi thanh toán
            request.session['cart'] = {}
            # Chuyển hướng đến trang thành công sau khi nhập liệu
            return redirect('home')

    else:
        form = CheckoutForm()

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    total_quantity = 0
    total_price = Decimal('0.00')
    # Get cart items from the order if it exists
    if order:
        items = order.orderproduct_set.all()
        total_quantity = order.get_cart_items
        total_price = order.get_cart_total
    else:
        items = []
        
    return render(request, 'app/checkout.html', {'form': form ,'items': items,'total_quantity': total_quantity,'total_price': total_price})


def product_detail(request, id):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.orderproduct_set.all()
        cartItems = order.get_cart_items
    else:
        items=[]
        order={'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
    products = Product.objects.filter(id=id)
    categories = Category.objects.filter(is_sub=False)
    context = {'products': products, 'categories': categories, 'items': items, 'order': order, 'CartItems': cartItems}
    return render(request, 'app/product_detail.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productID']
    action = data['action']
    customer = request.user
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

def register(request):
    form = CreaterUserForm()
    if request.method == "POST":
        form = CreaterUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context={'form': form}
    return render(request,'app/register.html', context)

def loginuser(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else: messages.info(request,'Tài khoản hoặc mật khẩu chưa đúng')

    context={}
    return render(request,'app/login.html', context)

def logoutuser(request):
    logout(request)
    return redirect('login')

def search(request):
    searched = ''
    keys = []
    cartItems = 0
    if request.method == "POST":
        searched = request.POST['searched']
        keys = Product.objects.filter(name__icontains=searched)
        
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.orderproduct_set.all()
        cartItems = order.get_cart_items
    else:
        items=[]
        order={'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
  
    Products = Product.objects.all()
    return render(request, 'app/search.html',{'searched':searched,'keys':keys,'cartItems':cartItems,'Products': Products})


