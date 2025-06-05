from django.urls import path
from api.views import (
    search_for_collection,
)

urlpatterns = [
    path("search-products/", search_for_collection, name="search-products"),
   
]