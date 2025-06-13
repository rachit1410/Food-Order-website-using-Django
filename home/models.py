from django.db import models
import uuid
from accounts.models import Seller, Customer
from home.choices import STAR_CHOICES
from django.db.models.signals import post_save
from django.dispatch import receiver


class Base(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(Base):
    category = models.CharField(max_length=255, unique=True)
    category_icon = models.FileField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category


class SubCategory(Base):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    sub_catagory_name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('category', 'sub_catagory_name')

    def __str__(self):
        return f"{self.category.category} - {self.sub_catagory_name}"


class Brand(Base):
    brand = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.brand


class Images(Base):
    image = models.ImageField(upload_to="item_images")

    def __str__(self):
        return self.image.name if self.image else "No Image"


class Item(Base):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="my_items")
    sku = models.CharField(max_length=255, unique=True)
    item_name = models.CharField(max_length=255)
    item_description = models.TextField()
    item_price = models.FloatField(default=1)
    item_image = models.ForeignKey(Images, related_name="item_primary_image", on_delete=models.SET_NULL, null=True, blank=True)
    item_discount_percentage = models.IntegerField(default=0)
    item_subcategory = models.ForeignKey(SubCategory, related_name="items", on_delete=models.SET_NULL, null=True, blank=True)
    item_brand = models.ForeignKey(Brand, related_name="brand_items", on_delete=models.CASCADE)
    rating = models.FloatField(default=1.0)
    quantity = models.CharField(max_length=255)

    def __str__(self):
        return self.item_name


class VariantItem(Base):
    item = models.ForeignKey(Item, related_name="variants", on_delete=models.CASCADE)
    variant_name = models.CharField(max_length=255)
    item_image = models.ForeignKey(Images, related_name="variant_image", on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.CharField(max_length=255)
    price = models.FloatField(default=1)
    sku = models.CharField(max_length=255, unique=True)
    discount_percentage = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.item.item_name} - {self.variant_name}"


class Reviews(Base):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="my_reviews")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="reviews")
    stars = models.CharField(max_length=10, choices=STAR_CHOICES)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Review by {self.customer.username} for {self.item.item_name}"


class Cart(Base):
    customer = models.ForeignKey(Customer, related_name="my_cart", on_delete=models.CASCADE)
    total_price = models.FloatField(default=0.00)

    def __str__(self):
        return f"Cart of {self.customer.username}"


class CartItem(Base):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    item = models.ForeignKey(Item, related_name="carts", on_delete=models.CASCADE, null=True, blank=True)
    item_quantity = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.cart.customer.username}'s cart item: {self.item.item_name}"


@receiver(post_save, sender=CartItem)
def update_cart_total_price(sender, instance, **kwargs):
    discounted_price = instance.item.item_price - (instance.item.item_price * instance.item.item_discount_percentage / 100)
    CartItem.objects.filter(pk=instance.pk).update(
        total_price=discounted_price * instance.item_quantity
    )
    cart = instance.cart
    total = sum(
        (cartitem.item.item_price - (cartitem.item.item_price * cartitem.item.item_discount_percentage / 100)) * cartitem.item_quantity
        for cartitem in cart.cart_items.all() if cartitem.item
    )
    Cart.objects.filter(pk=cart.pk).update(total_price=int(total))


class WishList(Base):
    customer = models.ForeignKey(Customer, related_name="my_wishlist", on_delete=models.CASCADE)

    def __str__(self):
        return f"Wishlist of {self.customer.username}"


class WishlistItems(Base):
    wishlist = models.ForeignKey(WishList, on_delete=models.CASCADE, related_name="wish_items")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="wishlists")
    item_availability = models.BooleanField(default=True)

    def __str__(self):
        return f"item {self.item.item_name} of wishlist of {self.wishlist.customer.username}"


class Status(Base):
    status = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.status


class CustomerOrder(Base):
    customer = models.ForeignKey(Customer, related_name="my_orders", on_delete=models.CASCADE)
    status = models.ForeignKey(Status, related_name='order_status', on_delete=models.SET_NULL, null=True, blank=True)
    total_amount = models.IntegerField(default=0)

    def __str__(self):
        return f"Order {self.uuid} by {self.customer.username}"


class OrderItem(Base):
    item = models.ForeignKey(Item, related_name="item_in_orders", on_delete=models.CASCADE)
    order = models.ForeignKey(CustomerOrder, related_name="order_items", on_delete=models.CASCADE)
    total_price = models.IntegerField(default=0)

    def __str__(self):
        return f"item {self.item.item_name} Ordered by {self.order.customer.username}"


class Collection(Base):
    collection_name = models.CharField(max_length=255, unique=True)
    items = models.ManyToManyField(Item, related_name="item_collections")
    seller = models.ForeignKey(Seller, related_name="my_collections", on_delete=models.CASCADE)
    collection_logo = models.OneToOneField(Images, related_name="collection_logo_of", on_delete=models.SET_NULL, null=True, blank=True)
    collection_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.collection_name


class MostSearched(Base):
    search = models.CharField(max_length=225)
    times_searched = models.IntegerField(default=1)
