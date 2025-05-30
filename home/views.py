from django.shortcuts import render, redirect
from accounts.models import Seller, Customer
from django.contrib.auth.decorators import login_required
from home.utils import get_is_seller
from home.models import Collection


def home(request):
    is_seller = None
    is_logged_in = request.user.is_authenticated 
    if is_logged_in:   
        is_seller = get_is_seller(request)
    context = {
        'is_logged_in': is_logged_in,
        'is_seller': is_seller
    }

    return render(request, "home/home.html", context)


def about_us(request):
    return render(request, "home/about_us.html")


def contact_us(request):
    return render(request, "home/contact_us.html")


def item_detail(request, pk):
    return render(request, "home/product_detail.html")


def search_filter(request):
    return render(request, "home/search_filter.html")


def check_out(request):
    return render(request, "home/check_out.html")


def card_pay(request):
    return render(request, "home/card-pay.html")


def upi_pay(request):
    return render(request, "home/upi-pay.html")


def cart(request):
    return render(request, "home/cart.html")


def thank(request):
    return render(request, "home/thankyou.html")


def not_found(request):
    return render(request, "404.html")


@login_required(login_url="login")
def my_collections(request):
    if get_is_seller(request):
        collections = Collection.objects.filter(seller__id=request.user.id)
        context = {
            "collections": collections
        }
        return render(request, "home/list_my_collections.html", context)
    return redirect("home")

def create_collection(request):
    if get_is_seller(request):
        return render(request, "home/create_collection.html")
