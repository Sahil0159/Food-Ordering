from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
# Create your views here.

#@login_required(login_url="/login/")
def home(request):
    pizza=Product.objects.all()
    image=ProductImages.objects.all()
    context={'zipped':zip(pizza,image)}
    return render(request,'home.html',context)

def login_page(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        if not User.objects.filter(username=username).exists():
            messages.error(request,'Invalid username')
            return redirect('/login/')
        user=authenticate(username=username,password=password)
        if user is None:
            messages.error(request,'password is incorrect')
            return redirect('/login/')
        else:
            login(request,user)
            return redirect('/')
        
    return render(request,'login.html')

def register_page(request):
    if request.method=="POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=User.objects.filter(username=username)
        if user.exists():
            messages.info(request,"Username alrady taken")
            return redirect("/register/")
        user=User.objects.create(first_name=first_name,last_name=last_name,username=username)
        user.set_password(password)
        user.save()
        messages.info(request,'account created successfully')
        return redirect('/register/')
    return render(request,"register.html")

def logout_page(request):
    logout(request)
    return redirect('/login/')
