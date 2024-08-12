from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login , logout
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from .models import *
from decimal import Decimal
#CSRF_EXCEMPT DECORATOR
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
# Create your views here.
def index(request):
    products = Products.objects.all()
    return render(request, "index.html", {"products" : products})

def form(request):
    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]
        price = request.POST["price"]
        image = request.POST["image"]
        Products.objects.create(name=name, description=description, price=price, image=image)

    return render(request, "form.html")


@csrf_exempt
@login_required
def addtocart(request, product_id):
    user = request.user
    product = Products.objects.get(id = product_id)
    if Cart.objects.filter(user=user, product=product).exists():
        cart = Cart.objects.get(user=user, product=product)
        cart.quantity += 1
        cart.total = int(cart.product.price * cart.quantity)
        cart.save()
    
        total_sum =Cart.objects.aggregate(total_sum=Sum('total'))['total_sum']
        if Payment.objects.filter(user=user).exists():
            payment = Payment.objects.get(user = user)
            payment.amount = total_sum
            payment.save()
        else:
            Payment.objects.create(user=user, amount=total_sum)
        total_tax = int(total_sum * 0.05)
        sub_total = int(total_sum + total_tax)
        return JsonResponse({"success": "Cart item quantity increased", "quantity": cart.quantity, "total": cart.total , "total_sum": total_sum, "total_tax": total_tax, "sub_total":sub_total})
    else:  
        Cart.objects.create(user=user, product=product ,total=product.price)
        return JsonResponse({"success": "Cart item added "})

def product(request):
    products = products.objects.all()
    return render (request, "product.html", {"products" : products})

@login_required
def cart(request):
    
    subtotal = Decimal('0')
    cart_items = Cart.objects.filter(user = request.user)
    tax = Decimal('0.05')
    shipping_charges = 10
    for item in cart_items:
        subtotal = subtotal + item.total
    tax = subtotal * tax
    total = subtotal + tax + shipping_charges
    return render (request, "cart.html", {"cart_items": cart_items, "subtotal": subtotal, 'tax':tax, 'shipping_charges':shipping_charges, 'total':total})

def payment(request):
    payment = Payment.objects.get(user=request.user)
    cart = Cart.objects.filter(user=request.user)
    return render (request, "payment.html",{"payment": payment, "cart": cart})

def product_detail(request):
    return render (request, "product_detail.html")

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = authenticate(request, username=username, password=password)
        print (user)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': 'Login successful'})
        else:
            return JsonResponse({'error': 'Invalid credentials'})
    return render(request,'login_user.html')


def logout_user(request):
    logout(request)
    return redirect("home")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        
        if User.objects.filter(username=username).exists():
            return JsonResponse ({"error": "this username is already exists"})
        elif User.objects.filter(email=email).exists():
            return JsonResponse ({"error": "this email is already exists"})
        
        else :
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            
            if user != None:
               return redirect("login") 
        
    return render (request, "register.html")
    

@csrf_exempt
def removefromcart(request, product_id):
    product = Products.objects.get(id=product_id)
    cart = Cart.objects.get(product=product, user=request.user)
    cart.delete()
    return JsonResponse({"success": "Item is removed"})

@csrf_exempt
def decrease_quantity(request,product_id):
    if request.method == "POST":
        product = Products.objects.get(id=product_id)
        cart = Cart.objects.get(product=product, user=request.user)
        cart.quantity -= 1
        cart.total = int(cart.product.price * cart.quantity)
        cart.save()
        total_sum =Cart.objects.aggregate(total_sum=Sum('total'))['total_sum']
        total_tax = int(total_sum * 0.05)
        sub_total = int(total_sum + total_tax)
        return JsonResponse({"success": "Cart item quantity increased", "quantity": cart.quantity, "total": cart.total , "total_sum": total_sum, "total_tax": total_tax, "sub_total":sub_total})
   
