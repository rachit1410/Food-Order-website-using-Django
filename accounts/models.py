from django.db import models
from django.contrib.auth.models import User
from accounts.choices import COUNTRY_CHOICES
import uuid


class Address(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    house_number = models.CharField(max_length=254, null=True, blank=True)
    colony = models.CharField(max_length=254, null=True, blank=True)
    nearby_place = models.CharField(max_length=254, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100, choices=COUNTRY_CHOICES, default="India")

    def __str__(self):
        return f"{self.colony}, {self.nearby_place}, {self.city}, {self.state}, {self.postal_code}, {self.country}"


class Seller(User):
    gst_number = models.CharField(max_length=100, unique=True)
    shop_id = models.CharField(max_length=100, unique=True)
    bmp_id = models.CharField(max_length=100, unique=True)
    shop_location = models.ForeignKey(Address, related_name="seller", on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=100)
    seller_name = models.CharField(max_length=100)
    shop_name = models.CharField(max_length=100)
    is_seller = models.BooleanField(default=True, editable=False)
    is_varified = models.BooleanField(default=True)
    business_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.shop_name

    class Meta:
        verbose_name = "Seller"


class Customer(User):
    phone_number = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    address = models.ForeignKey(Address, related_name="customer", on_delete=models.SET_NULL, null=True, blank=True)
    is_seller = models.BooleanField(default=False, editable=False)

    class Meta:
        verbose_name = "Customer"
