from django.shortcuts import render


def home(request):
    is_logged_in = request.user.is_authenticated

    context = {
        'is_logged_in': is_logged_in
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
