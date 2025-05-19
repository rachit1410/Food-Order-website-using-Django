from django.urls import path
from accounts.views import (
    register_customer,
    register_seller,
    login,
    my_account,
)

urlpatterns = [
    path('register-seller/', register_seller, name="register-seller"),
    path('register-customer/', register_customer, name="register-customer"),
    path('login/', login, name="login"),
    path('my-account/', my_account, name="my-account"),
]
