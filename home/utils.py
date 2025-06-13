import requests
from io import BytesIO
from django.core.files import File
from django.db import transaction
import pandas as pd
import random
import string
import lorem
import logging

from home.models import Images, Category, SubCategory, Brand, Item, VariantItem, Cart, MostSearched
from accounts.models import Seller
from home.models import Collection
from uuid import UUID
from django.db.models import Q
from django.utils import timezone


def save_image_from_url(image_url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        response = requests.get(image_url, stream=True, headers=headers)
        response.raise_for_status()

        file_name = image_url.split("/")[-1]
        file_ext = file_name.split(".")[-1]
        if file_ext not in ['jpg', 'jpeg', 'png', 'gif']:
            file_name = "image.jpg"
        else:
            file_name = f"image.{file_ext}"

        image_content = BytesIO(response.content)

        img = Images()
        img.image.save(file_name, File(image_content))
        img.save()
        return img

    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
        return None
    except Exception as e:
        print(f"Error saving image: {e}")
        return None


def get_discount(mrp_str, selling_price_str):
    """Calculates discount percentage from MRP and selling price strings."""
    try:
        new_mrp = float(mrp_str.split(" ")[1])
        new_sp = float(selling_price_str.split(" ")[1])

        if new_mrp <= 0:
            return 0
        return int(100 - (new_sp * 100 / new_mrp))
    except (ValueError, IndexError):
        logging.warning(f"Could not parse MRP '{mrp_str}' or Selling Price '{selling_price_str}'. Returning 0% discount.")
        return 0


def get_rating():
    """Generates a random rating between 3.0 and 4.9."""
    return round(random.uniform(3.0, 4.9), 1)


def get_sku(product_name, unique_skus):
    """Generates a unique SKU based on product name and random digits."""
    base_sku = ''.join(word[0].upper() for word in product_name.split() if word)

    if not base_sku:  # Fallback for empty product names
        base_sku = "PROD"

    # Ensure uniqueness
    sku = base_sku + ''.join(random.choices(string.digits, k=4))
    while sku in unique_skus:
        sku = base_sku + ''.join(random.choices(string.digits, k=4))
    unique_skus.append(sku)
    return sku


def get_description():
    """Generates a random lorem ipsum description."""
    length = random.randint(10, 30)
    return ' '.join([lorem.sentence() for _ in range(length)])


# --- Main Data Import Function ---

def exceltodatabase():
    file_path = "C:/Users/RD/OneDrive/Documents/Projects/FODE/FODE/BigBasket_Dataset.csv.xlsx"
    file_df = pd.read_excel(file_path)
    product_names = []
    unique_skus = []
    for index, row in file_df.iterrows():
        try:
            with transaction.atomic():
                if row['Sku name'] not in product_names:
                    category, _ = Category.objects.get_or_create(category=row['Category'])
                    sub_category, _ = SubCategory.objects.get_or_create(sub_catagory_name=row['Sub-Category'], category=category)
                    brand, _ = Brand.objects.get_or_create(brand=row['Brand'])
                    seller = Seller.objects.get(username="rachit")
                    product_name = row['Sku name']
                    image_url = row['Image']
                    mrp = row['MRP']
                    selling_price = row['Selling Price']
                    discount = get_discount(mrp, selling_price)
                    price = int(mrp.split(" ")[1])
                    rating = get_rating()
                    sku = get_sku(product_name, unique_skus)
                    description = get_description()
                    quantity = row['Product Size']
                    image = save_image_from_url(image_url)
                    item = Item.objects.create(
                        seller=seller,
                        sku=sku,
                        item_name=product_name,
                        item_description=description,
                        item_price=price,
                        item_discount_percentage=discount,
                        item_subcategory=sub_category,
                        item_brand=brand,
                        rating=rating,
                        quantity=quantity,
                        item_image=image,
                    )

                    product_names.append(row['Sku name'])
                    print(product_name, " DONE ")
                else:
                    item = Item.objects.filter(item_name=row['Sku name'])[0]
                    item_image = save_image_from_url(row['Image'])
                    variant_name = row['Sku name']
                    quantity = row['Product Size']
                    mrp = row['MRP']
                    selling_price = row['Selling Price']
                    discount = get_discount(mrp, selling_price)
                    price = int(mrp.split(" ")[1])
                    sku = get_sku(product_name=variant_name, unique_skus=unique_skus)
                    discount_percentage = get_discount(mrp_str=mrp, selling_price_str=selling_price)

                    duplicate_varient = VariantItem.objects.filter(variant_name=variant_name, quantity=quantity)

                    if quantity == item.quantity or duplicate_varient.exists():
                        continue
                    else:
                        VariantItem.objects.create(
                            item=item,
                            item_image=item_image,
                            variant_name=variant_name,
                            quantity=quantity,
                            discount_percentage=discount_percentage,
                            price=price,
                            sku=sku,
                        )

                        print(variant_name, " DONE ")

        except Exception as e:
            print(e)
            continue


def get_is_seller(request):
    user = None
    if Seller.objects.filter(pk=request.user.pk).exists():
        user = Seller.objects.get(pk=request.user.pk)
    if user:
        return True
    return False


def get_discounted_price(price, discount):
    if discount and price:
        return int(price-(price*discount/100))
    return 0


def get_all_collections():
    return Collection.objects.all()


def get_cart_total(request):
    try:
        cart = Cart.objects.get(customer__id=request.user.id)
        return cart.total_price
    except Cart.DoesNotExist:
        print("not customer")
        return 0


def is_wishlisted(request, product):
    """
    Returns True if the current user has wishlisted the given product, else False.
    Assumes a related_name='wishlists' on the wishlist-product relationship.
    """
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        return False
    return product.wishlists.filter(wishlist__customer__pk=user.pk).exists()


def add_to_searched(query):
    if MostSearched.objects.filter(search=query).exists():
        searched = MostSearched.objects.filter(search=query)[0]
        searched.times_searched += 1
        searched.save()
    else:
        MostSearched.objects.create(
            search=query
        )


def get_searched():
    thirty_days_ago = timezone.now() - pd.Timedelta(days=30)
    MostSearched.objects.filter(created_at__lt=thirty_days_ago).delete()
    return MostSearched.objects.all().order_by("-times_searched")[:20]


def cc():
    try:
        return Collection.objects.get(uuid=UUID("efdab293-897c-4b82-b082-16537f7ecf07"))
    except Collection.DoesNotExist:
        return None


def cm():
    try:
        return Collection.objects.get(uuid=UUID("51db04da-2496-4c48-9004-a723cdfb7b00"))
    except Collection.DoesNotExist:
        return None


def tc():
    try:
        return Collection.objects.get(uuid=UUID("a209e2e5-2c01-4b67-967b-6d359f00b333"))
    except Collection.DoesNotExist:
        return None


def sd():
    try:
        return Collection.objects.get(uuid=UUID("90f63050-e150-4e24-9e2d-5e4956bbbec9"))
    except Collection.DoesNotExist:
        return None


def ccc():
    try:
        return Collection.objects.filter(
            Q(uuid=UUID("9e312a37-e078-48b8-ade2-8ec4fdcf528c")) |
            Q(uuid=UUID("b1248e5c-ced0-4287-aed4-9c4ba9f47c5f")) |
            Q(uuid=UUID("36e5a6a4-b57b-49af-8bae-cd076f450b8a"))
        ).order_by("created_at")
    except Collection.DoesNotExist:
        return None


def trendingItems():
    items = Item.objects.filter(Q(item_subcategory__category__category="BAKERY, CAKES AND DAIRY") | Q(Q(item_subcategory__category__category="BEVERAGES"))).order_by("-rating")[:30]
    catitems = {
        "BAKERY, CAKES AND DAIRY": [],
        "BEVERAGES": []
    }
    categories = Category.objects.filter(Q(category="BEVERAGES") | Q(category="BAKERY, CAKES AND DAIRY"))
    for item in items:
        category = item.item_subcategory.category.category
        catitems[category].append(item)

    return {"items": items, "catitems": catitems, "categories": categories}


def most_popular():
    items = Item.objects.all().order_by("-rating")[:8]
    return items


def just_arived():
    items = Item.objects.filter(item_brand__brand__icontains="Fresho").order_by("-created_at")[:8]
    return items
