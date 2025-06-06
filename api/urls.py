from django.urls import path
from api.views import (
    search_for_collection,
    add_to_cart,
    add_to_wishlist
)

urlpatterns = [
    path("search-products/", search_for_collection, name="search-products"),
    path("add-to-wishlist/", add_to_cart, name="add-to-wishlist"),
    path("add-to-cart/", add_to_wishlist, name="add-to-cart"),
]
