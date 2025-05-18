from django.urls import path
from home.views import (
    home,
    about_us,
    contact_us,
    item_detail,
    search_filter,
    check_out,
)


urlpatterns = [
    path("", home, name="home"),
    path("about-us/", about_us, name="about-us"),
    path("contact-us/", contact_us, name="contact-us"),
    path("item-detail/<pk>/", item_detail, name="item-detail"),
    path("search-filter/", search_filter, name="search_filter"),
    path("check-out/<pk>/", check_out, name="check-out"),
]
