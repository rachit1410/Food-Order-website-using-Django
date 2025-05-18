from django.db import models
from django.contrib.auth.models import User


class Address(models.Model):
    street_number = models.CharField(max_length=254)
    street_name = models.CharField(max_length=254)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street_number} {self.street_name}, {self.city}, {self.state}, {self.postal_code}, {self.country}"


class Seller(User, models.Model):
    gst_number = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    address = models.ForeignKey(Address, related_name="seller", on_delete=models.CASCADE)
    is_seller = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['gst_number', 'phone_number', 'company_name']

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = "Seller"


class Customer(User, models.Model):
    phone_number = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    address = models.ForeignKey(Address, related_name="customer", on_delete=models.SET_NULL, null=True, blank=True)
    is_seller = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'name']

    class Meta:
        verbose_name = "Customer"
