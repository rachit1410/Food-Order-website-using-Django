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
    category = models.CharField(max_length=255, unique=True) # Added unique=True
    
    class Meta:
        verbose_name_plural = "Categories" # Corrected verbose_name_plural

    def __str__(self):
        return self.category


class SubCategory(Base):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories") # Changed related_name
    sub_catagory_name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('category', 'sub_catagory_name') # Added unique_together for better data integrity

    def __str__(self):
        return f"{self.category.category} - {self.sub_catagory_name}"


class Brand(Base):
    brand = models.CharField(max_length=255, unique=True) # Added unique=True

    def __str__(self):
        return self.brand


class Images(Base):
    image = models.ImageField(upload_to="item_images")

    def __str__(self):
        return self.image.name if self.image else "No Image"


class Item(Base):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="my_items") # Changed related_name
    sku = models.CharField(max_length=255, unique=True) # Added unique=True
    item_name = models.CharField(max_length=255)
    item_description = models.TextField()
    item_price = models.FloatField(default=1)
    item_image = models.ForeignKey(Images, related_name="item_primary_image", on_delete=models.SET_NULL, null=True, blank=True) # Changed related_name and on_delete
    item_discount_percentage = models.IntegerField(default=0)
    item_category = models.ForeignKey(SubCategory, related_name="items", on_delete=models.SET_NULL, null=True, blank=True)
    item_brand = models.ForeignKey(Brand, related_name="brand_items", on_delete=models.CASCADE)
    rating = models.FloatField(default=5.0)
    quantity = models.CharField(max_length=255) # Consider changing to IntegerField or DecimalField if always numeric

    def __str__(self):
        return self.item_name


class VariantItem(Base):
    item = models.ForeignKey(Item, related_name="variants", on_delete=models.CASCADE)
    variant_name = models.CharField(max_length=255)
    item_image = models.ForeignKey(Images, related_name="variant_image", on_delete=models.SET_NULL, null=True, blank=True) # Changed related_name and on_delete
    quantity = models.CharField(max_length=255) # Consider changing to IntegerField or DecimalField
    price = models.FloatField(default=1)
    sku = models.CharField(max_length=255, unique=True) # Added unique=True
    discount_percentage = models.IntegerField(default=0)


    def __str__(self):
        return f"{self.item.item_name} - {self.variant_name}"


class Reviews(Base):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="my_reviews") # Changed related_name
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="reviews") # Added item foreign key
    stars = models.CharField(max_length=10, choices=STAR_CHOICES)
    comment = models.TextField(blank=True, null=True) # Added a comment field
    images = models.ForeignKey(Images, related_name="review_images", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Review by {self.customer.username} for {self.item.item_name}"


class Cart(Base):
    customer = models.ForeignKey(Customer, related_name="my_cart", on_delete=models.CASCADE) # Changed related_name
    items = models.ForeignKey(Item, related_name="carts", on_delete=models.CASCADE)
    item_quantity = models.FloatField(default=1.00) # Changed default to float
    total_price = models.FloatField(default=0.00)

    def __str__(self):
        return f"Cart of {self.customer.username}"


class WishList(Base):
    customer = models.ForeignKey(Customer, related_name="my_wishlist", on_delete=models.CASCADE) # Changed related_name
    items = models.ForeignKey(Item, related_name="wishlisted_by", on_delete=models.CASCADE) # Changed related_name
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f"Wishlist of {self.customer.username}"


class Status(Base):
    status = models.CharField(max_length=255, unique=True) # Added unique=True

    def __str__(self):
        return self.status


class CustomerOrder(Base):
    customer = models.ForeignKey(Customer, related_name="my_orders", on_delete=models.CASCADE) # Changed related_name
    items = models.ManyToManyField(Item, related_name="orders") # Changed to ManyToManyField for multiple items in an order
    status = models.ForeignKey(Status, related_name='order_status', on_delete=models.SET_NULL, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True) # Added order_date
    total_amount = models.FloatField(default=0.00) # Added total_amount

    def __str__(self):
        return f"Order {self.uuid} by {self.customer.username}"


class Collection(Base):
    collection_name = models.CharField(max_length=255, unique=True) # Added unique=True
    items = models.ManyToManyField(Item, related_name="item_collections")
    collection_logo = models.OneToOneField(Images, related_name="collection_logo_of", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.collection_name