from decimal import Decimal
from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import *
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordChangeView
from django.views import generic
import uuid
from django.conf import settings
from django.core.mail import send_mail


def aboutme(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        cartItems = order.get_cart_items
    else:
        order={'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
    categories = Category.objects.filter(is_sub = False)
    context={'CartItems': cartItems, 'categories':categories}
    return render(request, 'app/about_me.html', context)
#Category
def category(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        cartItems = order.get_cart_items
    else:
        order={'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category','')
    if active_category:
        products = Product.objects.filter(category__slug=active_category)
    context={'categories': categories, 'products': products, 'active_category':active_category, 'CartItems': cartItems}
    return render(request,'app/category.html',context)
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        cartItems = order.get_cart_items
    else:
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
        if request.user.is_authenticated:
            customer = request.user
            order = Order.objects.get(customer=customer, complete=False)
            cart_items = order.orderproduct_set.all()
            form = CheckoutForm(request.POST)
            if form.is_valid():
                # Lấy dữ liệu từ form
                customer_name = form.cleaned_data['customer_name']
                email = form.cleaned_data['email']
                address = form.cleaned_data['address']
                phone_number = form.cleaned_data['phone_number']
                # Tạo CustomerPurchase
                purchase = CustomerPurchase.objects.create(
                    customer_name=customer_name,
                    address=address,
                    phone_number=phone_number,
                    email = email
                )
                # Lưu thông tin sản phẩm từ giỏ hàng vào CustomerPurchase
                products = []  # Khởi tạo danh sách để lưu thông tin sản phẩm
                quantitys = []
                prices = []
                for item in cart_items:
                    product = item.product  # Lấy thông tin sản phẩm từ item trong vòng lặp
                    product_name = product.name
                    quantity = item.quantity
                    price = product.price
                    PurchaseItem.objects.create(
                        customer_purchase=purchase,
                        product=product,
                        quantity=quantity,
                        price=price  # Sử dụng giá của sản phẩm từ item
                    )
                    
                    products.append(product_name)  # Thêm thông tin sản phẩm vào danh sách
                    quantitys.append(quantity)
                    prices.append(price)
                # Sử dụng danh sách sản phẩm trong hàm send_mail_after_checkout hoặc ở bất kỳ đâu cần thiết
                send_mail_after_checkout(email, customer_name, products, quantitys, prices)

                # Đánh dấu đơn hàng đã hoàn thành
                order.complete = True
                order.save()
                # Xóa giỏ hàng sau khi thanh toán
                cart_items.delete()
                # Chuyển hướng đến trang thành công sau khi nhập liệu
                return redirect('home')
        else:
            return redirect('login')
    else:
        if request.user.is_authenticated:
            customer = request.user
            order = Order.objects.get(customer=customer, complete=False)
            cartItems = order.get_cart_items
            form_data = {
                'customer_name': customer.first_name,
                'email': customer.email,
                'address': customer.address,
                'phone_number': customer.phone_number,
            }
            form = CheckoutForm(initial=form_data)
        else:
            return redirect('login')

    total_quantity = 0
    total_price = Decimal('0.00')
    if order:
        customer_name = customer.first_name
        email = customer.email
        items = order.orderproduct_set.all()
        total_quantity = order.get_cart_items
        total_price = order.get_cart_total
    else:
        items = []   
    return render(request, 'app/checkout.html', {'form': form ,'items': items,'total_quantity': total_quantity,'total_price': total_price,'CartItems': total_quantity})


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
        product.quantity -= 1
    elif action == 'remove':
        orderProduct.quantity -= 1
        product.quantity += 1
    if orderProduct.quantity <= 0:
        orderProduct.delete()
    else:
        orderProduct.save()
    product.save()
    
    return JsonResponse('added', safe=False)

def register(request):
    
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        try:
            if CustomUser.objects.filter(username = username).first():
                messages.success(request,'Tên tài khoản đã tồn tại')
                return redirect('/register')
            if CustomUser.objects.filter(email = email).first():
                messages.success(request,'Email đã tồn tại')
                return redirect('/register')
            if (password1 != password2):
                messages.success(request,'Mật khẩu phải trùng nhau')
                return redirect('/register')
            
            user_obj = CustomUser.objects.create(first_name = first_name, last_name = last_name, username = username, email = email, phone_number = phone_number, address = address)
            user_obj.set_password(password1)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj= Profile.objects.create(user = user_obj, auth_token = auth_token)
            profile_obj.save()
            send_mail_after_registration(email , auth_token, username)
            return redirect('/token_send')
        except Exception as e:
            print(e)
    return render(request,'app/register.html')

def loginuser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = CustomUser.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request, 'Tên đăng nhập hoặc mật khẩu sai')
            return redirect('/login')
        profile_obj = Profile.objects.filter(user = user_obj ).first()
        if not profile_obj.is_verified:
            messages.success(request, 'Tài khoản chưa xác minh, vui lòng kiểm tra Email của bạn')
            return redirect('/login')

        user = authenticate(request, username=username, password = password)
        
        if user and not user.is_superuser:
            login(request, user)
            return redirect('dashboard')
        else: messages.success(request,'Tài khoản hoặc mật khẩu chưa đúng')

    context={}
    return render(request,'app/login.html', context)

def logoutuser(request):
    logout(request)
    return redirect('login')

def search(request):
    searched = ''
    keys = []

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        cartItems = order.get_cart_items
    else:
        order={'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']


    if request.method == "POST":
        searched = request.POST['searched']
        keys = Product.objects.filter(name__icontains=searched)
        
    categories = Category.objects.filter(is_sub = False)
    Products = Product.objects.all()
    context={'searched':searched,'keys':keys,'cartItems':cartItems,'Products': Products, 'categories':categories}
    return render(request, 'app/search.html',context)


def dashboard(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        cartItems = order.get_cart_items
    else:
        order={'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
    categories = Category.objects.filter(is_sub = False)
    Products = Product.objects.all()
    context={'categories': categories,'Products': Products, 'CartItems': cartItems}
    return render(request,'app/dashboard.html', context)



class PasswordchangeView(PasswordChangeView):
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('password_success')

def password_success(request):
    return render(request, "app/password_change_success.html")

class UpdateUserView(generic.UpdateView):
    form_class = EditUserForm
    template_name = "app/edit_profile.html"
    success_url = reverse_lazy('editprofile')

    def get_object(self):
        return self.request.user
    
def purchased_products(request):
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
    return render(request,'app/purchased_product.html', context)
def token_send(request):
    return render (request, 'app/token_send.html')

def success(request):
    return render (request, 'app/success.html')

def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Tài khoản của bạn đã xác minh')
                return redirect('/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Tài khoản của bạn đã xác minh')
            return redirect('/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')

def send_mail_after_registration(email , token, username):
    subject = 'Tài khoản của bạn cần phải xác minh'
    message = f'Xin chào đây là đường dẫn xác minh tài khoản {username} tại Shop Sports http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )


def send_mail_after_checkout(email, customer_name, products, quantities, prices):
    subject = 'Đơn hàng'
    # Tạo nội dung email dưới dạng HTML
    message = f'''
        <p>Xin chào, đây là đơn hàng của khách hàng <b>{customer_name}</b> tại Shop Sports:</p>
        <table border="1" style="width:500px;">
            <tr>
                <th>Tên sản phẩm</th>
                <th>Số lượng</th>
                <th>Giá</th>
            </tr>
    '''

    # Duyệt qua các sản phẩm và thêm vào bảng trong email
    for product, quantity, price in zip(products, quantities, prices):
        message += f'''
            <tr>
                <td>{product}</td>
                <td>{quantity}</td>
                <td>{price} VNĐ</td>
            </tr>
        '''

    message += '''
        </table>
    '''
    
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]

    # Gửi email với nội dung được định dạng HTML
    send_mail(subject, '', email_from, recipient_list, html_message=message)