from django.urls import path
from home.views import (
    home,
    about_us,
    contact_us,
    item_detail,
    search_filter,
    check_out,
    cart,
    upi_pay,
    card_pay,
    thank,
    not_found,
    my_collections,
    create_collection
)

urlpatterns = [
    path("", home, name="home"),
    path("about-us/", about_us, name="about-us"),
    path("contact-us/", contact_us, name="contact-us"),
    path("item-detail/<pk>/", item_detail, name="item-detail"),
    path("search/", search_filter, name="search"),
    path("check-out/", check_out, name="check-out"),
    path("my-cart/", cart, name="my-cart"),
    path("upi-gateway/", upi_pay, name="upi-gateway"),
    path("card-gateway/", card_pay, name="card-gateway"),
    path("thank-you/", thank, name="thank-you"),
    path("404/", not_found, name="404"),
    path("manage-collections/", my_collections, name="manage-collections"),
    path("create-collections/", create_collection, name="create-collections"),
]
