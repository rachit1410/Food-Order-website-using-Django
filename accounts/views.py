from django.shortcuts import render, redirect
from accounts.models import Customer, Address
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
import re
from django.contrib.auth.decorators import login_required


def register_customer(request):
    if request.method == "POST":
        full_name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        # Regular expressions for validation
        name_regex = r"^[a-zA-Z\s]+$"
        username_regex = r"^[a-zA-Z0-9_]{5,}$"
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        # Validate input
        if not re.match(name_regex, full_name):
            messages.error(request, "Invalid name. Only letters and spaces are allowed.")
            return redirect('register-customer')

        if not re.match(username_regex, username):
            messages.error(request, "Invalid username. Must be at least 5 characters, alphanumeric and underscore.")
            return redirect('register-customer')

        if not re.match(email_regex, email):
            messages.error(request, "Invalid email address.")
            return redirect('register-customer')

        if Customer.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect('register-customer')

        if Customer.objects.filter(email=email).exists():
            messages.error(request, "Account associated with the given email already exists.")
            return redirect('register-customer')

        address = Address.objects.create()

        user = Customer.objects.create(
            name=full_name,
            username=username,
            phone_number=phone_number,
            email=email,
            address=address
        )
        user.set_password(password)
        user.save()

        return redirect('login')

    return render(request, "accounts/register_customer.html")


def register_seller(request):
    return render(request, "accounts/register_seller.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, "accounts/login.html")


@login_required
def logout_view(request):
    try:
        logout(request)
        return redirect('home')
    except Exception as e:
        print(e)
        return redirect('home')


@login_required()
def my_account(request):
    try:
        account = Customer.objects.get(pk=request.user.pk)
        if request.method == "POST":
            if 'name' in request.POST:
                account.name = request.POST.get('name')
                account.phone_number = request.POST.get('phone_number')
                account.save()
                messages.success(request, "Profile updated")

            elif 'postal_code' in request.POST:
                address = Address.objects.get(pk=account.address.pk)
                address.postal_code = request.POST.get('postal_code')
                address.nearby_place = request.POST.get('nearby_place')
                address.colony = request.POST.get('colony')
                address.city = request.POST.get('city')
                address.state = request.POST.get('state')
                address.country = request.POST.get('country')
                address.save()
                messages.success(request, "Address updated")

            elif 'new_password1' in request.POST:
                new_password1 = request.POST.get('new_password1')
                new_password2 = request.POST.get('new_password2')
                if new_password1 == new_password2:
                    account.set_password(new_password1)
                    account.save()
                    update_session_auth_hash(request, account)
                    messages.success(request, 'password changed successfully')
                else:
                    messages.error(request, "Passwords do not match")
            return redirect('my-account')  # Redirect after *any* POST action
        context = {
            "profile": {
                "name": account.name,
                "username": account.username,
                "email": account.email,
                "phone_number": account.phone_number,
                "address": {
                        "postal_code": account.address.postal_code,
                        "colony": account.address.colony,
                        "nearby_place": account.address.nearby_place,
                        "city": account.address.city,
                        "state": account.address.state,
                        "country": account.address.country,
                    }
                }
        }

        return render(request, "accounts/myaccountcustomer.html", context)
    except Exception as e:
        print(e)
        messages.error(request, "Something went wrong")
        return redirect('home')
