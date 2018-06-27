from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
# Create your views here.
def signup(request):
    if request.method == 'POST':
        # The user wants to sign up!
        error = None
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                error = 'Username has already been taken'
                return render(request, 'accounts/signup.html',{'error':error})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                auth.login(request,user)
                return redirect('home')
        else:
            error = 'Passwords must match'
            return render(request, 'accounts/signup.html',{'error':error})
    else:
        # User wants to enter info
        return render(request,'accounts/signup.html')

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return  render(request, 'accounts/login.html',{'error':'username or password is incorrect'})
    else:
        return render(request,'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
