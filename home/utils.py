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
    """
    Downloads an image from a URL and saves it to the Images model.
    Handles common errors and ensures a valid file extension.
    """
    if not image_url:
        logging.warning("Received empty image URL. Skipping image download.")
        return None

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        response = requests.get(image_url, stream=True, headers=headers, timeout=10) # Added timeout
        response.raise_for_status()

        # Extract filename and extension, ensure a default if none
        file_name = os.path.basename(image_url).split('?')[0] # Remove query parameters from URL
        if '.' not in file_name:
            file_name = "image.jpg" # Default filename if no extension
        else:
            name, ext = os.path.splitext(file_name)
            if not ext or ext.lower() not in ['.jpg', '.jpeg', '.png', '.gif']:
                file_name = f"{name}.jpg" # Ensure a valid extension

        image_content = BytesIO(response.content)

        img = Images()
        img.image.save(file_name, File(image_content), save=True) # save=True is default, but explicit
        logging.info(f"Successfully saved image: {file_name}")
        return img

    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading image from {image_url}: {e}")
        return None
    except Exception as e:
        logging.error(f"Error saving image from {image_url}: {e}")
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
    unique_skus.add(sku)
    return sku


def get_description():
    """Generates a random lorem ipsum description."""
    length = random.randint(10, 30)
    return ' '.join([lorem.sentence() for _ in range(length)])


# --- Main Data Import Function ---

def bulk_create_items_from_excel(file_path):
    """
    Reads item data from an Excel file and bulk creates/updates items, variants, and images.
    """
    try:
        file_df = pd.read_excel(file_path)
    except FileNotFoundError:
        logging.error(f"File not found at: {file_path}")
        return
    except Exception as e:
        logging.error(f"Error reading Excel file: {e}")
        return

    # Pre-fetch common objects to minimize database queries inside the loop
    try:
        seller = Seller.objects.get(username="seller") # Ensure this seller exists
    except Seller.DoesNotExist:
        logging.error("Seller with username 'seller' not found. Please create this seller first.")
        return

    # Dictionaries to hold objects for bulk creation and to track created items
    items_to_create = []
    variants_data_for_bulk_create = [] # Hold dictionaries of variant data
    images_to_process = {} # Store image URL -> (item_name, is_variant, obj_sku_or_name)
    
    # Store unique SKUs generated to prevent collisions
    unique_item_skus = set(Item.objects.values_list('sku', flat=True))
    unique_variant_skus = set(VariantItem.objects.values_list('sku', flat=True))

    BATCH_SIZE = 500 # Increased batch size for potentially better performance

    logging.info(f"Starting bulk creation process with batch size: {BATCH_SIZE}")

    # Use a dictionary to map product names to already created or pending Item objects
    # This helps in linking variants to the correct parent item
    item_cache = {} 

    for index, row in file_df.iterrows():
        try:
            # Get or create Category, SubCategory, Brand - These are relatively few and can be handled
            # outside the main bulk processing for items/variants if preferred for very large datasets
            # but get_or_create is generally efficient enough for these lookups.
            category, _ = Category.objects.get_or_create(category=row['Category'])
            sub_category, _ = SubCategory.objects.get_or_create(sub_catagory_name=row['Sub-Category'], category=category)
            brand, _ = Brand.objects.get_or_create(brand=row['Brand'])
            
            product_name = str(row['Sku name']).strip() # Ensure string and strip whitespace
            image_url = str(row['Image']).strip()
            mrp = str(row['MRP']).strip()
            selling_price = str(row['Selling Price']).strip()
            quantity = str(row['Product Size']).strip() # This is the variant name for your structure

            # Common data for both Item and VariantItem
            discount = get_discount(mrp, selling_price)
            price = float(mrp.split(" ")[1]) if " " in mrp else float(mrp) # Handle cases where " " might not be present
            rating = get_rating()
            description = get_description()

            # Check if an item with this product_name already exists or is pending creation
            # We use product_name as the grouping key for items
            item_obj = item_cache.get(product_name)

            if not item_obj:
                # If no item exists or is pending, create a new Item
                item_sku = get_sku(product_name, unique_item_skus)
                item_obj = Item(
                    seller=seller,
                    sku=item_sku,
                    item_name=product_name,
                    item_description=description,
                    item_price=price,
                    item_discount_percentage=discount,
                    item_category=sub_category,
                    item_brand=brand,
                    rating=rating,
                    quantity=quantity # The initial quantity for the base item
                )
                items_to_create.append(item_obj)
                item_cache[product_name] = item_obj # Add to cache for subsequent variants
                images_to_process[item_obj.sku] = {'url': image_url, 'is_variant': False, 'obj_name': product_name}
                logging.debug(f"Prepared Item for creation: {product_name} (SKU: {item_sku})")
            else:
                # If an item already exists or is pending, treat this as a variant
                variant_sku = get_sku(f"{product_name}-{quantity}", unique_variant_skus) # More specific SKU for variants
                variants_data_for_bulk_create.append({
                    "parent_item_sku": item_obj.sku, # Store SKU to link after base items are saved
                    "variant_name": quantity,
                    "image_url": image_url,
                    "quantity": quantity,
                    "price": price,
                    "sku": variant_sku
                })
                images_to_process[variant_sku] = {'url': image_url, 'is_variant': True, 'obj_name': f"{product_name} - {quantity}"}
                logging.debug(f"Prepared Variant for creation: {product_name} - {quantity} (SKU: {variant_sku})")

            # Process batches
            if len(items_to_create) >= BATCH_SIZE:
                logging.info(f"Processing batch of {len(items_to_create)} items and {len(variants_data_for_bulk_create)} variants.")
                _process_batch(items_to_create, variants_data_for_bulk_create, images_to_process)
                
                # Clear lists for the next batch
                items_to_create = []
                variants_data_for_bulk_create = []
                images_to_process = {}
                item_cache = {} # Clear cache for next batch to avoid memory issues with huge files

        except KeyError as ke:
            logging.error(f"Missing column in Excel file: {ke} at row {index}. Skipping row.")
            continue
        except ValueError as ve:
            logging.error(f"Data conversion error: {ve} at row {index}. Check numeric fields. Skipping row.")
            continue
        except Exception as e:
            logging.error(f"Unhandled error processing row {index}: {e}. Skipping row.")
            continue

    # Process any remaining items after the loop
    if items_to_create:
        logging.info(f"Processing final batch of {len(items_to_create)} items and {len(variants_data_for_bulk_create)} variants.")
        _process_batch(items_to_create, variants_data_for_bulk_create, images_to_process)
    
    logging.info("Bulk creation process completed.")


def _process_batch(items_to_create, variants_data_for_bulk_create, images_to_process):
    """
    Helper function to process a batch of items, images, and variants within a transaction.
    """
    with transaction.atomic():
        logging.info("Bulk creating items...")
        # Bulk create items first
        Item.objects.bulk_create(items_to_create)
        logging.info(f"Successfully bulk created {len(items_to_create)} items.")

        # Re-fetch the created items to get their IDs, needed for ForeignKeys
        # Use the SKUs to fetch them efficiently
        created_item_skus = [item.sku for item in items_to_create]
        saved_items_map = {item.sku: item for item in Item.objects.filter(sku__in=created_item_skus)}

        # Process images and link them to items
        logging.info("Processing images for items...")
        for sku, img_data in images_to_process.items():
            image_url = img_data['url']
            is_variant = img_data['is_variant']
            obj_name = img_data['obj_name']

            img_obj = save_image_from_url(image_url)
            if img_obj:
                if not is_variant:
                    # Link image to the main Item
                    item_instance = saved_items_map.get(sku)
                    if item_instance:
                        item_instance.item_image = img_obj
                        item_instance.save(update_fields=['item_image'])
                        logging.debug(f"Linked image to Item: {obj_name}")
                    else:
                        logging.warning(f"Item with SKU {sku} not found for image linking.")
                # Variant images will be linked during VariantItem creation below
            else:
                logging.warning(f"Failed to download or save image for {obj_name} from URL: {image_url}")

        # Prepare VariantItem objects for bulk creation
        variants_for_bulk_create = []
        logging.info("Preparing variants for bulk creation...")
        for v_data in variants_data_for_bulk_create:
            parent_item_sku = v_data["parent_item_sku"]
            parent_item = saved_items_map.get(parent_item_sku) # Get the item instance from our map

            if parent_item:
                variant_image_url = v_data["image_url"]
                variant_sku = v_data["sku"]
                
                # Get the image object that was already processed for this variant's SKU
                # This assumes save_image_from_url was called and the image was saved
                img_obj_data = images_to_process.get(variant_sku)
                if img_obj_data:
                    # We need to fetch the Images object from DB as save_image_from_url creates and saves it
                    try:
                        variant_img = Images.objects.get(image__endswith=os.path.basename(img_obj_data['url']).split('?')[0])
                        # If a default image name was used, finding it by original URL basename might be tricky.
                        # A better way might be to return the created Images object from save_image_from_url and pass it around.
                    except Images.DoesNotExist:
                        logging.warning(f"Variant image for SKU {variant_sku} not found in DB after download. Skipping image link for variant.")
                        variant_img = None
                else:
                    variant_img = None


                variants_for_bulk_create.append(VariantItem(
                    item=parent_item,
                    variant_name=v_data["variant_name"],
                    item_image=variant_img, # Link the image here
                    quantity=v_data["quantity"],
                    price=v_data["price"],
                    sku=variant_sku
                ))
            else:
                logging.warning(f"Parent item with SKU {parent_item_sku} not found for variant '{v_data['variant_name']}'. Skipping variant creation.")

        if variants_for_bulk_create:
            logging.info(f"Bulk creating {len(variants_for_bulk_create)} variants...")
            VariantItem.objects.bulk_create(variants_for_bulk_create)
            logging.info("Successfully bulk created variants.")
        else:
            logging.info("No variants to bulk create in this batch.")
