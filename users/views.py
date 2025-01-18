from cmath import log
from tkinter import E
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.http import HttpResponseRedirect, HttpResponse
from .models import Profile

# Create your views here.
def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        usr_obj = User.objects.filter(username=email)

        if not usr_obj.exists():
            messages.warning(request, 'Account not found, Please register...')
            return HttpResponseRedirect(request.path_info)
        
        if not usr_obj[0].profile.is_email_verified:
            messages.warning(request, 'Your account is not verified, Please verify...')
            return HttpResponseRedirect(request.path_info)

        
        usr_obj = authenticate(username = email , password= password)
        if usr_obj:
            login(request , usr_obj)
            return redirect('home/')
        
        messages.warning(request, 'Invalid credentials.')
        return HttpResponseRedirect(request.path_info)
    return render(request, 'users/login.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        usr_obj = User.objects.filter(username=email)

        if usr_obj.exists():
            messages.warning(request, 'Email already registerd.')
            return HttpResponseRedirect(request.path_info)
        
        usr_obj = User.objects.create(first_name = first_name, last_name=last_name, email=email,username=email)
        usr_obj.set_password(password)
        usr_obj.save()
        messages.success(request, 'An email has been sent on registerd mail Id.')
        return HttpResponseRedirect(request.path_info)

    return render(request, 'users/register.html')


def activate_email(request , email_token):
    try:
        user = Profile.objects.get(email_token= email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/')
    except Exception as e:
        return HttpResponse('Invalid Email token')