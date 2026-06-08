# --- Admin Orders View ---
def admin_orders(request):
    return render(request, 'admin_orders.html')

# --- Admin Customers View ---
def admin_customers(request):
    return render(request, 'admin_customers.html')

# --- Admin Enquiries View ---
def admin_enquiries(request):
    return render(request, 'admin_enquiries.html')

# --- Admin Books View ---
def admin_books(request):
    return render(request, 'admin_books.html')
from django.shortcuts import render, redirect
from django.contrib import messages
from mainapp.models import * 
from .models import *
from useraap.models import *
from django.views.decorators.cache import cache_control
# Create your views here.
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def admindash(request):
    if 'adminid' not in request.session:
        messages.error(request, 'You need to log in as admin to access this page.')
        return redirect('adminlogin')
    adminid = request.session['adminid']
    recent_orders = Order.objects.order_by('-ordered_at')[:5]
    orders_data = []
    for order in recent_orders:
        orders_data.append({
            'id': order.id,
            'customer_name': order.user.name if hasattr(order.user, 'name') else str(order.user),
            'date': order.ordered_at.strftime('%Y-%m-%d %H:%M'),
            'status': 'Completed',  # You can update this if you have a status field
            'total': order.total_amount,
        })
    context = {
        'adminid': adminid,
        'orders_count': Order.objects.count(),
        'customers_count': UserInfo.objects.count(),
        'enquiries_count': Enquiry.objects.count(),
        'books_count': Book.objects.count(),
        'recent_orders': orders_data,
    }
    return render(request, 'admindash.html', context)

def adminlogout(request):
    if 'adminid' in request.session:
        del request.session['adminid']
        messages.success(request, 'You have been logged out successfully.')
    else:
        messages.error(request, 'You are not logged in.')
    return redirect('adminlogin')

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def viewenqs(request):
    if 'adminid' not in request.session:
        messages.error(request, 'You need to log in as admin to access this page.')
        return redirect('adminlogin')
    adminid = request.session['adminid']
    enqs= Enquiry.objects.all()  # Assuming you have an Enquiry model
    context = {
        'adminid': adminid,
        'enqs': enqs,
    }
    return render(request, 'viewenqs.html',context)


def delenq(request,id):
    if 'adminid' not in request.session:
        messages.error(request, 'You need to log in as admin to access this page.')
        return redirect('adminlogin')
    enq= Enquiry.objects.get(id=id)
    enq.delete()  # Delete the enquiry
    messages.success(request, 'Enquiry deleted successfully.')
    return redirect( 'viewenqs')

    # Assuming you have an Enquiry model

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def addcat(request):
    if 'adminid' not in request.session:
        messages.error(request, 'You need to log in as admin to access this page.')
        return redirect('adminlogin')
    adminid = request.session['adminid']
    context = {
        'adminid': adminid,
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        # created_at =request.POST.get('created_at')
        cat=Category(name=name, description=description,)
        cat.save()  # Save the category to the database
        messages.success(request, 'Category added successfully.')
        return redirect('addcat')

    return render(request, 'addcat.html',context)

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def viewcat(request):
    if 'adminid' not in request.session:
        messages.error(request, 'You need to log in as admin to access this page.')
        return redirect('adminlogin')
    adminid = request.session['adminid']
    context = {
        'adminid': adminid,
    }
    return render(request, 'viewcat.html',context)

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def addbook(request):
    if 'adminid' not in request.session:
        messages.error(request, 'You need to log in as admin to access this page.')
        return redirect('adminlogin')
    adminid = request.session['adminid']
    cats=Category.objects.all()

    context = {
        'adminid': adminid,
        'cats': cats,
    }
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        category = request.POST.get('category')
        cat = Category.objects.get(id=category)  # Get the category object
        description = request.POST.get('description')
        original_price = request.POST.get('original_price')
        price = request.POST.get('price')
        published_date = request.POST.get('published_date')
        language = request.POST.get('language')
        cover_image = request.FILES.get('image')
        stock = request.POST.get('stock')
        b = Book(
            title = title,
            author = author,
            category = cat,
            description = description,
            original_price = original_price,
            price = price,
            published_date = published_date,
            language = language,
            cover_image = cover_image,
            stock = stock,
        )
        b.save()
        messages.success(request, 'Book addition is scuccessful.')
        return redirect('addbook')
    return render(request, 'addbook.html',context)

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def viewbook(request):
    if 'adminid' not in request.session:
        messages.error(request, 'You need to log in as admin to access this page.')
        return redirect('adminlogin')
    adminid = request.session['adminid']
    context = {
        'adminid': adminid,
    }
    return render(request, 'viewbook.html',context)

# function to veiw categories in viewcat.html
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def viewcat(request):
    if 'adminid' not in request.session:
        messages.error(request, "You need to log in as admin first.")
        return redirect('adminlogin')
    adminid= request.session.get('adminid')
    enqs= Category.objects.all()
    context = {
        'adminid': adminid,
        'enqs': enqs,
    }
    return render(request, 'viewcat.html', context)
# function to delete a category
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def delcat(request,id):
    if 'adminid' not in request.session:
        messages.error(request, "You need to log in as admin first.")
        return redirect('adminlogin')
    enq = Category.objects.get(id=id)
    enq.delete()
    messages.success(request, "One Category was deleted successfully.")
    return redirect('viewcat')

# function to veiw books in viewbook.html
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def viewbook(request):
    if 'adminid' not in request.session:
        messages.error(request, "You need to log in as admin first.")
        return redirect('adminlogin')
    adminid= request.session.get('adminid')
    books = Book.objects.all()
    context = {
        'adminid': adminid,
        'books': books,
    }
    return render(request, 'viewbook.html', context)

# function to delete a book.
def delbook(request,id):
    if 'adminid' not in request.session:
        messages.error(request, "You need to log in as admin first.")
        return redirect('adminlogin')
    book = Book.objects.get(id=id)
    book.delete()
    messages.success(request, "One Category was deleted successfully.")
    return redirect('viewbook')

# function to change password
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def change_pwd(request):
    if 'adminid' not in request.session:
        messages.error(request, 'You need to log in as admin to access this page.')
        return redirect('adminlogin')
    adminid = request.session['adminid']
    msg = None
    if request.method == 'POST':
        old_pwd = request.POST.get('old_password')
        new_pwd = request.POST.get('new_password')
        confirm_pwd = request.POST.get('confirm_password')
        try:
            admin_login = LoginInfo.objects.get(username=adminid, usertype='admin')
            if admin_login.password != old_pwd:
                msg = 'Old password is incorrect.'
            elif new_pwd != confirm_pwd:
                msg = 'New password and confirm password do not match.'
            else:
                admin_login.password = new_pwd
                admin_login.save()
                msg = 'Password changed successfully.'
        except LoginInfo.DoesNotExist:
            msg = 'Admin account not found.'
    context = {
        'adminid': adminid,
        'msg': msg,
    }
    return render(request, 'change_pwd.html', context)

# function to edit book
def editbook(request, id):
    if 'adminid' not in request.session:
        messages.error(request, 'You need to log in as admin to access this page.')
        return redirect('adminlogin')
    adminid = request.session['adminid']
    book= Book.objects.get(id=id)
    cats=Category.objects.all()
    context = {
        'adminid': adminid,
        'book': book,
        'cats': cats,
    }
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        category = request.POST.get('category')
        cat = Category.objects.get(id=category)  # Get the category object
        description = request.POST.get('description')
        original_price = request.POST.get('original_price')
        price = request.POST.get('price')
        published_date = request.POST.get('published_date')
        language = request.POST.get('language')
        cover_image = request.FILES.get('image')
        stock = request.POST.get('stock')
        # Update the book object with new data
        book.title = title
        book.author = author
        book.category = cat
        book.description = description
        book.original_price = original_price
        book.price = price
        if published_date:
            book.published_date = published_date
        book.language = language
        if cover_image:
            book.cover_image = cover_image
        book.stock = stock
        book.save()
        messages.success(request, f"{title} has been updated successfully.")
        return redirect('viewbook')
    return render(request, 'editbook.html',context)

