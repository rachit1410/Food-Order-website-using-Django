from django.shortcuts import render, redirect
from accounts.models import Customer, Address, Seller
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from home.models import Cart, WishList
from home.utils import get_is_seller


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

        if Seller.objects.filter(email=email).exists():
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

        Cart.objects.create(customer=user)
        WishList.objects.create(customer=user)

        return redirect('login')

    return render(request, "accounts/register_customer.html")


def register_seller(request):
    if request.method == "POST":
        gst_number = request.POST.get("gst_number")
        shop_id = request.POST.get("shop_id")
        bmp_id = request.POST.get("bmp_id")
        shop_name = request.POST.get("shop_name")
        business_description = request.POST.get("business_description")
        seller_name = request.POST.get('seller_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        house_number = request.POST.get("house_number")
        colony = request.POST.get("colony")
        nearby_place = request.POST.get("nearby_place")
        city = request.POST.get("city")
        state = request.POST.get("state")
        postal_code = request.POST.get("postal_code")
        country = request.POST.get("country", "India")

        # Regular expressions for validation
        seller_name__regex = r"^[a-zA-Z\s]+$"
        username_regex = r"^[a-zA-Z0-9_]{5,}$"
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        # Validate input
        if not password == confirm_password:
            messages.error(request, "password and confirm password does not match.")
            return redirect('register-seller')

        if not re.match(seller_name__regex, seller_name):
            messages.error(request, "Invalid name. Only letters and spaces are allowed.")
            return redirect('register-seller')

        if not re.match(username_regex, username):
            messages.error(request, "Invalid username. Must be at least 5 characters, alphanumeric and underscore.")
            return redirect('register-seller')

        if not re.match(email_regex, email):
            messages.error(request, "Invalid email address.")
            return redirect('register-seller')

        if Seller.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect('register-seller')

        if Customer.objects.filter(email=email).exists():
            messages.error(request, "Account associated with the given email already exists.")
            return redirect('register-seller')

        address = Address.objects.create(
            house_number=house_number,
            colony=colony,
            nearby_place=nearby_place,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
        )

        user = Seller.objects.create(
            username=username,
            gst_number=gst_number,
            shop_id=shop_id,
            bmp_id=bmp_id,
            shop_location=address,
            phone_number=phone_number,
            seller_name=seller_name,
            shop_name=shop_name,
            business_description=business_description,
        )
        user.set_password(password)
        user.save()

        return redirect('login')
    return render(request, "accounts/register_seller.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if username is None and email is not None:
            username = User.objects.filter(email=email)[0].username

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
                address.house_number = request.POST.get('house_number')
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
            return redirect('my-account')
        from home.models import Category
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
            },
            "user": {
                "is_seller": get_is_seller(request),
                "is_logged_in": True,
                "categories": Category.objects.all()
            }
        }

        return render(request, "accounts/myaccountcustomer.html", context)
    except Exception as e:
        print(e)
        messages.error(request, "Something went wrong")
        return redirect('home')


def my_account_seller(request):
    try:
        account = Seller.objects.get(pk=request.user.pk)
        if request.method == "POST":
            if 'name' in request.POST:
                account.seller_name = request.POST.get('name')
                account.phone_number = request.POST.get('phone_number')
                account.business_description = request.POST.get('bussiness_description')
                account.save()
                messages.success(request, "Profile updated")

            elif 'postal_code' in request.POST:
                address = Address.objects.get(pk=account.shop_location.pk)
                address.house_number = request.POST.get('house_number')
                address.postal_code = request.POST.get('postal_code')
                address.nearby_place = request.POST.get('nearby_place')
                address.colony = request.POST.get('colony')
                address.city = request.POST.get('city')
                address.state = request.POST.get('state')
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
            return redirect('my-account-seller')
        context = {
            "profile": {
                "name": account.seller_name,
                "username": account.username,
                "email": account.email,
                "phone_number": account.phone_number,
                "gst_number": account.gst_number,
                "shop_id": account.shop_id,
                "bmp_id": account.bmp_id,
                "shop_name": account.shop_name,
                "business_description": account.business_description,
                "address": {
                        "house_number": account.shop_location.house_number,
                        "postal_code": account.shop_location.postal_code,
                        "colony": account.shop_location.colony,
                        "nearby_place": account.shop_location.nearby_place,
                        "city": account.shop_location.city,
                        "state": account.shop_location.state,
                        "country": account.shop_location.country,
                    }
                }
        }

        return render(request, "accounts/myaccountseller.html", context)
    except Exception as e:
        print(e)
        messages.error(request, "Something went wrong")
        return redirect('home')


def upload_view(request):
    return render(request, "accounts/upload_file.html")
