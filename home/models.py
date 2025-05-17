from django.db import models
import uuid
from accounts.models import Seller, Customer
from home.choices import STAR_CHOICES


class Base(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(Base):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = "Catagorie"


class Brand(Base):
    brand = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class Images(Base):
    image = models.ImageField(upload_to="item_images")


class Item(Base):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="myitems")
    item_name = models.CharField(max_length=100)
    item_description = models.TextField()
    item_price = models.FloatField(default=1)
    item_discount_persentage = models.IntegerField(default=0)
    item_category = models.ForeignKey(Category, related_name="items", on_delete=models.SET_NULL, null=True, blank=True)
    item_Brand = models.ForeignKey(Category, related_name="brand_items", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    item_images = models.ForeignKey(Images, related_name="image_item", on_delete=models.SET_NULL, null=True, blank=True)


class Reviews(Base):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="myitems")
    stars = models.CharField(max_length=10, choices=STAR_CHOICES)
    images = models.ForeignKey(Images, related_name="image_by", on_delete=models.SET_NULL, null=True, blank=True)


class Cart(Base):
    customer = models.ForeignKey(Customer, related_name="mycart", on_delete=models.CASCADE)
    items = models.ForeignKey(Item, related_name="carts", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=True)
    total_price = models.FloatField(default=0.00)

    def __str__(self):
        return f"cart of {self.customer.name}"


class WishList(Base):
    customer = models.ForeignKey(Customer, related_name="mywishliat", on_delete=models.CASCADE)
    items = models.ForeignKey(Item, related_name="wishlister", on_delete=models.CASCADE)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f"wishlist of {self.customer.name}"


class Status(Base):
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.status


class CustomerOrder(Base):
    customer = models.ForeignKey(Customer, related_name="myorders", on_delete=models.CASCADE)
    items = models.ForeignKey(Item, related_name="orders", on_delete=models.CASCADE)
    status = models.ForeignKey(Status, related_name='status_order', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"order of {self.customer.name}"
