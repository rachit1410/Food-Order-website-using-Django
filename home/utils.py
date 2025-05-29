import requests
from io import BytesIO
from django.core.files import File
from django.db import transaction
import pandas as pd
import random
import string
import lorem
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Import your models
from home.models import Images, Category, SubCategory, Brand, Item, VariantItem
from accounts.models import Seller # Assuming Seller is in accounts.models

# --- Helper Functions ---

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

        img = Images()  # assign item here
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
        # Extract numeric value and convert to float
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
    if not base_sku: # Fallback for empty product names
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
                    seller = Seller.objects.get(username="seller")
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
                    item = Item.objects.create(
                        seller=seller,
                        sku=sku,
                        item_name=product_name,
                        item_description=description,
                        item_price=price,
                        item_discount_percentage=discount,
                        item_category=sub_category,
                        item_brand=brand,
                        rating=rating,
                        quantity=quantity
                    )
                    save_image_from_url(image_url)
                    
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
                    
                    VariantItem.objects.create(
                            item = item,
                            item_image = item_image,
                            variant_name = variant_name,
                            quantity = quantity,
                            discount_percentage = discount_percentage,
                            price = price,
                            sku = sku,
                    )
                    
                    print(variant_name, " DONE ")
                    
                    
        except Exception as e:
            print(e)
            continue

