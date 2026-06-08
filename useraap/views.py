# Function to change user password

from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages 
from mainapp.models import *
from adminapp.models import *
from django.views.decorators.cache import cache_control
# Create your views here.
# payment
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    if 'userid' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')

    userid = request.session.get('userid')
    user = UserInfo.objects.get(email=userid)
    cart = Cart.objects.get(user=user)
    items = CartItem.objects.filter(cart=cart)

    line_items = []

    for item in items:
        line_items.append({
            'price_data': {
                'currency': 'inr',
                'unit_amount': int(item.book.price * 100),
                'product_data': {
                    'name': item.book.title,
                },
            },
            'quantity': item.quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card', 'sepa_debit'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri('/useraap/payment_success/'),
        cancel_url=request.build_absolute_uri('/viewcart/'),
    )

    return redirect(session.url, code=303)


def payment_success(request):
    if 'userid' not in request.session:
        messages.error(request, "Please login first.")
        return redirect('login')

 
    userid=request.session.get('userid')
    user = UserInfo.objects.get(email=userid)

    try:
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items.exists():
            messages.warning(request, "No items found in your cart.")
            return redirect('index')

  
        total_amount = sum(item.get_total_price() for item in cart_items)
        order = Order.objects.create(user=user, total_amount=total_amount)

        # Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price,
            )
            book = Book.objects.get(id = item.book.id)
            book.stock = book.stock - item.quantity
            book.save()
       
        cart_items.delete()

        items = OrderItem.objects.filter(order=order)

        # Add total_price attribute to each item
        for item in items:
            item.total_price = item.quantity * item.price

        
        messages.success(request, "Payment successful! Your order has been placed.")
        return render(request, 'payment_success.html', {'order': order})

    except Cart.DoesNotExist:
        messages.error(request, "Cart not found.")
        return redirect('index')

# end payment

def userdash(request):
    if 'userid' not in request.session:
        messages.error(request, "You are not logged-in.")
        return redirect('login')
    userid = request.session.get('userid')
    user = UserInfo.objects.get(email=userid)
    context = {
        'userid':userid,
        'user': user,
     }
    return render(request, 'userdash.html',context)

def userlogout(request):
    if 'userid' in request.session:
        del request.session['userid']
        messages.success(request, "You are logged-out successfully.")
        return redirect('index')
    else:
        messages.error(request,"Login first")   
        return redirect('index')
# function to viewcart
from django.views.decorators.cache import cache_control
def viewcart(request):
    if 'userid' not in request.session:
        messages.error(request, "You are not logged-in.")
        return redirect('login')
    userid = request.session.get('userid')
    user = UserInfo.objects.get(email=userid)
    ucart = Cart.objects.filter(user=user)
    if not ucart.exists():
        Cart.objects.create(user = user)
    cart = Cart.objects.get(user = user)
    items = CartItem.objects.filter(cart = cart)
    total_amount = 0
    for i in items:
        total_amount = i.get_total_price() 
    context = {
        'userid':userid,
        'user': user,
        'items': items,
        'total_amount' : total_amount,
     }
    return render(request, 'viewcart.html',context) 

# Function to userprofile
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def userprofile(request):
    if 'userid' not in request.session:
        messages.error(request, "You are not logged-in.")
        return redirect('login')
    userid = request.session.get('userid')
    user = UserInfo.objects.get(email=userid)
    context = {
        'userid':userid,
        'user': user,
     }
    return render(request, 'userprofile.html',context)

# Function to user orders
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def userorders(request):
    if 'userid' not in request.session:
        messages.error(request, "You are not logged-in.")
        return redirect('login')
    userid = request.session.get('userid')
    user = UserInfo.objects.get(email=userid)
    orders = Order.objects.filter(user=user)
    orderitems = []
    for o in orders:
        orderitems.append(OrderItem.objects.filter(order=o))

    context = {
        'userid':userid,
        'user': user,
        'orderitems':orderitems,
     }
    return render(request, 'userorders.html',context)

# Function to edit profile
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def editprofile(request):
    if 'userid' not in request.session:
        messages.error(request, "You are not logged-in.")
        return redirect('login')
    userid = request.session.get('userid')
    user = UserInfo.objects.get(email=userid)
    context = {
        'userid':userid,
        'user': user,
     }
    return render(request, 'editprofile.html',context)

# Fucntion for add to cart
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def addtocart(request, id):
    if 'userid' not in request.session:
        messages.error(request, "You are not logged-in.")
        return redirect('login')
    userid = request.session.get('userid')
    user = UserInfo.objects.get(email=userid)
    ucart = Cart.objects.filter(user=user)
    if not ucart.exists():
        Cart.objects.create(user = user)
    ucart = Cart.objects.get(user = user)
    book = Book.objects.get(id=id)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if quantity is None:
            quantity = 1
        ci = CartItem(cart = ucart, book=book, quantity=quantity)
        ci.save()
        messages.success(request, f"Book {book.title} is added to your cart.")
        return redirect('viewcart')
    else:
        messages.error(request, "Something went wrong")
        return redirect('index')
    

def removeitems(request,id):
    if 'userid' not in request.session:
        messages.error(request, "You are not logged-in.")
        return redirect('login')
    userid = request.session.get('userid')
    user = UserInfo.objects.get(email=userid)
    ci = CartItem.objects.get(id = id)
    ci.delete() 
    messages.success(request, "Book removed from Cart")
    return redirect('viewcart')

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def user_ch_pwd(request):
    if 'userid' not in request.session:
        messages.error(request, 'You need to log in to access this page.')
        return redirect('login')
    userid = request.session['userid']
    msg = None
    if request.method == 'POST':
        old_pwd = request.POST.get('old_password')
        new_pwd = request.POST.get('new_password')
        confirm_pwd = request.POST.get('confirm_password')
        try:
            user_login = LoginInfo.objects.get(username=userid, usertype='user')
            if user_login.password != old_pwd:
                msg = 'Old password is incorrect.'
            elif new_pwd != confirm_pwd:
                msg = 'New password and confirm password do not match.'
            else:
                user_login.password = new_pwd
                user_login.save()
                msg = 'Password changed successfully.'
        except LoginInfo.DoesNotExist:
            msg = 'User account not found.'
    context = {
        'userid': userid,
        'msg': msg,
    }
    return render(request, 'user_ch_pwd.html', context)