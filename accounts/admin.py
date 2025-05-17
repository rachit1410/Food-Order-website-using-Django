from django.contrib import admin
from accounts.models import (
    Address,
    Seller,
    Customer
)

admin.site.register(Address)
admin.site.register(Seller)
admin.site.register(Customer)
