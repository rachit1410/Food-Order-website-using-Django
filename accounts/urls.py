from django.urls import path
from accounts.views import (
    register_customer,
    register_seller,
    login_view,
    logout_view,
    my_account,
    my_account_seller,
    upload_view
)

urlpatterns = [
    path('register-seller/', register_seller, name="register-seller"),
    path('register-customer/', register_customer, name="register-customer"),
    path('login/', login_view, name="login"),
    path('my-account/', my_account, name="my-account"),
    path('my-account-seller/', my_account_seller, name="my-account-seller"),
    path('upload/', upload_view, name="upload"),
    path('logout/', logout_view, name="logout"),
]
