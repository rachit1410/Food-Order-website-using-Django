from django.shortcuts import render


def home(request):
    return render(request, "home/home.html")


def about_us(request):
    return render(request, "home/about_us.html")


def contact_us(request):
    return render(request, "home/contact_us.html")


def item_detail(request, pk):
    return render(request, "home/product_detail.html")


def search_filter(request):
    return render(request, "home/search_filter.html")


def check_out(request, pk):
    return render(request, "home/check_out.html")
