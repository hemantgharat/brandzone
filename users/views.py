from cmath import log
from tkinter import E
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .models import Profile
from django.contrib.auth.decorators import login_required
from .models import Profile, Address
from .forms import ProfileForm, AddressForm

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
        phone = request.POST.get('phone')

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


@login_required
def view_profile(request):
    user = request.user
    profile = user.profile  # Assuming OneToOne relation exists

    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'phone': profile.phone if profile else 'N/A',  # Handle case if profile is missing
    }
    return render(request, 'users/profile.html', context)


@login_required
def update_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    addresses = Address.objects.filter(user=request.user)

    if request.method == "POST":
        profile_form = ProfileForm(request.POST, instance=profile)
        address_form = AddressForm(request.POST)

        if profile_form.is_valid():
            profile_form.save()

        if address_form.is_valid():
            new_address = address_form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            print("Address added successfully...!")
            return redirect("update-profile")

    else:
        profile_form = ProfileForm(instance=profile)
        address_form = AddressForm()
    
    return render(request, "users/update-profile.html", {
        "profile_form": profile_form,
        "address_form": address_form,
        "addresses": addresses
    })

@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    return JsonResponse({"success": True})

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')
