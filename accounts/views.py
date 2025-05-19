from django.shortcuts import render


def register_customer(request):
    return render(request, "accounts/register_customer.html")


def register_seller(request):
    return render(request, "accounts/register_seller.html")


def login(request):
    return render(request, "accounts/login.html")


def my_account(request):
    return render(request, "accounts/myaccountcustomer.html")
