def search(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Book.objects.filter(title__icontains=query)
    context = {
        'results': results,
        'query': query,
        'userid': request.session.get('userid'),
    }
    return render(request, 'search_results.html', context)
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages 
from adminapp.models import *
from django.views.decorators.cache import cache_control
# Create your views here.

def index(request):

    context = {
        'books':Book.objects.all(),
        'new_arrivals': Book.objects.all()[:10],
        'userid' :request.session.get('userid'),
    }
    return render(request, 'index.html', context)
def about(request):
    context = {
        'userid' : request.session.get('userid'),
    }
    return render(request, 'about.html', context)
def contact(request):
   
    if request.method  == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        contactnumber=request.POST.get('contactnumber')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        # this is ORM(object relational mapping) in django
        # it is used to interact with the database
        # here we are creating an instance of the Enquiry model
        # and saving the data to the database
        enq = Enquiry(name=name, email=email, contactnumber=contactnumber, subject=subject, message=message)
        enq.save()
        messages.success(request, 'Your enquiry has been submitted successfully!')
        return redirect('contact')
    context = {
        'userid' : request.session.get('userid'),
        }
    return render(request, 'contact.html', context)
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        contactnumber = request.POST.get('contactnumber')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')
        # Check if the user already exists
        ch = LoginInfo.objects.filter(username=email)
        if ch.exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return redirect('register')
        # Create a new user
        log = LoginInfo(usertype='user', username=email, password=password)
        user = UserInfo(name=name, email=email, contactnumber=contactnumber, login=log)
        log.save()
        user.save()
        messages.success(request, 'Registration successful! You can now log in.')
        return redirect('register')
    context = {
        'userid' : request.session.get('userid'),
     }
    return render(request, 'register.html',context)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = LoginInfo.objects.get(username=username, password=password,usertype='user')
           
            if user is not None:
                request.session['userid'] = username # Store admin ID in session
                messages.success(request, f'Welcome {user.username}!')
                return redirect('index')
              # Redirect to admin dashboard
        except LoginInfo.DoesNotExist:
            messages.error(request, 'Invalid credentials. Please try again.')
            return redirect('login')
    context = {
        'userid' : request.session.get('userid'),
    }
    return render(request, 'login.html',context)
  
def service(request):
    context = {
        'userid' : request.session.get('userid'),
    }
    return render(request, 'service.html',context)
def adminlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = LoginInfo.objects.get(username=username, password=password)
           
            if user.status == 'active':
                request.session['adminid'] = username # Store admin ID in session
                messages.success(request, f'Welcome {user.username}!')
                return redirect('admindash')  # Redirect to admin dashboard
            else:
                messages.error(request, 'Your account is inactive.')
        except LoginInfo.DoesNotExist:
            messages.error(request, 'Invalid username or password.')
            return redirect('adminlogin')
    return render(request, 'adminlogin.html')
def adminlog(request):
    if request.method == 'POST':
        pass
    else:
        return redirect(request, 'adminlogin.html')
    
# function for book details page

def book_details(request, id):
    context = {
        'book': Book.objects.get(id=id),
        'userid' : request.session.get('userid'),
    }
    return render(request, 'book_details.html', context)