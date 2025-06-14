from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from home.utils import (get_is_seller, get_discounted_price, get_all_collections,
                        get_cart_total, is_wishlisted, cc, cm, tc, sd, ccc,
                        add_to_searched, get_searched, trendingItems, most_popular,
                        just_arived)
from home.models import (Collection, Category, Brand, SubCategory, Images, Item,
                         VariantItem, Reviews, Cart, CartItem, WishList, WishlistItems)
from accounts.models import Seller, Customer
from home.documents import ItemDocument
from elasticsearch_dsl import Q
from uuid import UUID
from django.contrib import messages
from django.http import JsonResponse
import json
from django.core.cache import cache
from django.views.decorators.cache import cache_page


@cache_page(60*15)
def home(request):
    is_seller = None
    is_logged_in = request.user.is_authenticated
    if is_logged_in:
        is_seller = get_is_seller(request)

    list_categories = Category.objects.all().order_by('category')
    context = {
        'is_logged_in': is_logged_in,
        'is_seller': is_seller,
        'cart_total': get_cart_total(request),
        'query': {
            "categories": list_categories
        },
        'data': {
          'collections': get_all_collections(),
          'featured': {
              'cc': cc(),
              "cm": cm(),
              "tc": tc(),
              "sd": sd(),
              "ccc": ccc(),
              "trending": trendingItems(),
              "most_popular": most_popular(),
              "just_arived": just_arived(),
          },
          'most_searches': get_searched()
        }
    }
    return render(request, "home/home.html", context)


def about_us(request):

    context = {
        "user": {
            "is_seller": get_is_seller(request),
            "is_logged_in": request.user.is_authenticated,
            "categories": Category.objects.all(),
            "cart_total": get_cart_total(request)
        },
    }

    return render(request, "home/about_us.html", context)


def contact_us(request):
    return render(request, "home/contact_us.html")


def item_detail(request, pk):
    try:
        categories = Category.objects.all()
        uuid = UUID(pk)
        if cache.get(pk):
            product = cache.get(pk)
        else:
            product = Item.objects.get(uuid=uuid)
            cache.set(pk, product, 60*10)

        # searching similar products
        if cache.get(pk+"variants"):
            variants = cache.get(pk+"variants")
        else:
            variants = VariantItem.objects.filter(item=product)
            cache.set(pk+"variants", variants, 60*10)

        reviews = Reviews.objects.filter(item=product)

        context = {
            "product": product,
            "reviews": reviews,
            "discounted_price": get_discounted_price(price=product.item_price, discount=product.item_discount_percentage),
            "user": {
                "is_seller": get_is_seller(request),
                "is_logged_in": request.user.is_authenticated,
                "categories": categories,
                "cart_total": get_cart_total(request)
            },
            "variant_products": variants,
            "is_wishlisted": is_wishlisted(request, product)
        }

        return render(request, "home/product_detail.html", context)
    except Exception as e:
        print(e)
        messages.error(request, "something went wrong.")
        return redirect("home")


def variant_detail(request, pk):
    try:
        categories = Category.objects.all()
        uuid = UUID(pk)

        if cache.get("variant"):
            variant = cache.get("variant")
        else:
            variant = VariantItem.objects.get(uuid=uuid)
            cache.set("variant", variant, 60*10)

        reviews = Reviews.objects.filter(item=variant.item)

        context = {
            "product": variant,
            "reviews": reviews,
            "discounted_price": get_discounted_price(price=variant.price, discount=variant.discount_percentage),
            "user": {
                "is_seller": get_is_seller(request),
                "is_logged_in": request.user.is_authenticated,
                "categories": categories
            }
        }

        return render(request, "home/variant_detail.html", context)
    except Exception as e:
        print(e)
        messages.error(request, "something went wrong.")
        return redirect("home")


def search_filter(request):

    is_seller = None
    is_logged_in = request.user.is_authenticated
    if is_logged_in:
        is_seller = get_is_seller(request)

    searched = request.GET.get("q", "")
    category = request.GET.get("cat", "")
    sub_cat = request.GET.get("subcat", "")
    brand = request.GET.get("br", "")
    min_price = request.GET.get("minp", "")
    max_price = request.GET.get("maxp", "")
    sort_by = request.GET.get("sort", "relevance")

    search = ItemDocument.search()

    if searched:
        if cache.get(searched):
            search = cache.get(searched)
        else:
            cache.set(searched, search, 60*10)

        search = search.query(
                Q(
                    "multi_match",
                    query=searched,
                    fields=[
                        "item_name",
                        "item_description",
                        "quantity",
                        "item_subcategory.sub_catagory_name",
                        "item_subcategory.category.category",
                        "item_brand.brand",
                    ],
                    fuzziness="AUTO"
                    )
                )
        # adding to recent searches
        add_to_searched(searched)

    if category != "":
        search = search.filter("match", item_subcategory__category__category=category)

    if sub_cat != "":
        search = search.filter("match", item_subcategory__sub_catagory_name=sub_cat)

    if brand != "":
        search = search.filter("match", item_brand__brand=brand)

    if min_price != "":
        search = search.filter("range", item_price={"gte": min_price})

    if max_price != "":
        search = search.filter("range", item_price={"lte": max_price})

    # sorting
    keyword_sort_fields = ["item_name", "item_description"]

    sort_field = sort_by.lstrip("-")
    if sort_field in keyword_sort_fields:
        sort_field = f"{sort_field}.keyword"

    if sort_by == "relevance" or not sort_by:
        search = search.sort("_score")
    elif sort_by.startswith("-"):
        search = search.sort({sort_field: {"order": "desc"}})
    else:
        search = search.sort({sort_field: {"order": "asc"}})

    total_items = search.count()

    # pagination
    page_number = int(request.GET.get("page", 1))
    per_page = 30
    start = (page_number - 1) * per_page
    previous = page_number > 1
    next = start + per_page < search.count()

    search = search[start:start + per_page]

    results = search.execute()

    products = []
    for hit in results:
        product = hit.to_dict()
        product['uuid'] = str(hit.meta.id)
        products.append(product)

    start_index = (page_number - 1) * per_page + 1
    end_index = start_index + len(results) - 1

    list_categories = Category.objects.all().order_by('category')

    # extraxting uuid and converting them into uuid object
    item_ids = [UUID(hit.meta.id) for hit in results if hasattr(hit.meta, "id")]
    list_brand = Brand.objects.filter(brand_items__in=item_ids).distinct()

    list_sub_category = SubCategory.objects.filter(category__category=category)

    context = {
        "query": {
            "searched": searched,
            "category": category,
            "brand": brand,
            "sub_cat": sub_cat,
            "min_price": min_price,
            "max_price": max_price,
            "sort_by": sort_by,
        },
        "query_list": {
            "categories": list_categories,
            "brands": list_brand,
            "sub_cats": list_sub_category,
            "is_logged_in": is_logged_in,
            "is_seller": is_seller,
            "cart_total": get_cart_total(request)
        },
        "data": {
            "count": total_items,
            "products": products
        },
        "page": {
            "page_number": page_number,
            "per_page": per_page,
            "previous": previous,
            "next": next,
            "start_index": start_index,
            "end_index": end_index,
        }
    }

    return render(request, "home/search_filter.html", context)


@login_required(login_url="login")
def check_out(request):
    if request.method == "POST":
        payment_method = request.POST.get("payment-method")

        if payment_method == "upi":
            return redirect("upi-gateway")
        elif payment_method == "card":
            return redirect("card-gateway")
        elif payment_method == "cod":
            return redirect("thank-you")
        else:
            return redirect("check-out")

    try:
        customer = Customer.objects.get(pk=request.user.pk)
        cart = Cart.objects.get(customer=customer)
        if cart.cart_items.all().count() == 0:
            return redirect("my-cart")

        context = {
            "customer": customer,
            "cart": cart,
            "user": {
                "categories": Category.objects.all(),
                "is_seller": get_is_seller(request),
                "is_logged_in": True
            }
        }

    except Exception as e:
        print(e)
        messages.error(request, "something went wrong. please try again later")
        return redirect("my-cart")
    return render(request, "home/check_out.html", context)


def card_pay(request):
    return render(request, "home/card-pay.html")


def upi_pay(request):
    return render(request, "home/upi-pay.html")


@login_required(login_url="login")
def cart(request):
    try:
        cart = Cart.objects.get(customer__id=request.user.id)

        if cart.cart_items.all().count() == 0:
            cart.total_price = 0
            cart.save()

        context = {
            "cart": cart,
            "user": {
                "is_seller": get_is_seller(request),
                "is_logged_in": True,
                "categories": Category.objects.all()
            }
        }
        return render(request, "home/cart.html", context)
    except Cart.DoesNotExist:
        print("not a customer")
        return redirect("home")


@login_required(login_url="login")
def remove_from_cart(request, pk):
    try:
        uuid = UUID(pk)
        cartitem = CartItem.objects.get(uuid=uuid)
        if cartitem:
            cartitem.cart.total_price = cartitem.cart.total_price - cartitem.total_price
            cartitem.cart.save()
            cartitem.delete()
        messages.success(request, "item removed successfully")
        return redirect("my-cart")
    except CartItem.DoesNotExist:
        messages.error(request, "Item not found.")
        return redirect("my-cart")


@login_required(login_url="login")
def Wishlist(request):
    try:
        wishList = WishList.objects.get(customer__id=request.user.id)
        context = {
            "wishlist": wishList,
            "user": {
                "is_seller": get_is_seller(request),
                "is_logged_in": True,
                "categories": Category.objects.all(),
                "cart_total": get_cart_total(request)
            }
        }
        return render(request, "home/wishlist.html", context)
    except WishList.DoesNotExist:
        print("not a customer")
        return redirect("home")


def add_to_wishlist(request, pk):
    try:
        uuid = UUID(pk)
        item = Item.objects.get(uuid=uuid)
        wishlist = WishList.objects.get(customer__pk=request.user.pk)
        if not WishlistItems.objects.filter(
                item=item,
                wishlist=wishlist
        ).exists():
            WishlistItems.objects.create(
                item=item,
                wishlist=wishlist
            )
            messages.success(request, "item added to wishlist.")
        else:
            messages.info(request, "already in the wishlist.")
        return redirect(request.META.get("HTTP_REFERER", "/"))
    except Exception as e:
        print(e)
        messages.error(request, "Something went wrong.")
        return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required(login_url="login")
def remove_from_wishlist(request, pk):
    try:
        uuid = UUID(pk)
        wishlistitem = WishlistItems.objects.get(uuid=uuid)
        if wishlistitem:
            wishlistitem.delete()
        messages.success(request, "item removed successfully")
        return redirect("wishlist")
    except CartItem.DoesNotExist:
        messages.error(request, "Item not found.")
        return redirect("wishlist")


def thank(request):
    return render(request, "home/thankyou.html")


@login_required(login_url="login")
def my_collections(request):
    if is_seller := get_is_seller(request):
        collections = Collection.objects.filter(seller__username=request.user.username)
        categories = Category.objects.all()
        data = []
        for collection in collections:
            data.append(
                {
                    "item_count": collection.items.count(),
                    "collection": collection
                }
            )

        context = {
            "data": data,
            "user": {
                "categories": categories,
                "is_seller": is_seller,
                "is_logged_in": True
            }
        }
        return render(request, "home/list_my_collections.html", context)
    return redirect("home")


@login_required(login_url="login")
def create_collection(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        cover = request.FILES.get("cover_image")

        items_json = request.POST.get("products")

        try:
            items = json.loads(items_json) if items_json else []
        except Exception:
            items = []

        image = Images.objects.create(
            image=cover
        )

        seller = Seller.objects.get(pk=request.user.pk)
        if Collection.objects.filter(collection_name=title).exists():
            return JsonResponse({
                "status": False,
                "message": "Collection name already exists."
            })

        collection = Collection.objects.create(
            collection_name=title,
            seller=seller,
            collection_logo=image,
            collection_description=description
        )

        for id in items:
            item_uuid = UUID(id)
            item = Item.objects.get(pk=item_uuid)
            collection.items.add(item)
        collection.save()

        return JsonResponse({
            "status": True,
            "message": "Collection created",
            "data": {}
        })

    if is_seller := get_is_seller(request):
        is_logged_in = request.user.is_authenticated
        categories = Category.objects.all()
        context = {
            "query_list": {
                "is_logged_in": is_logged_in,
                "is_seller": is_seller,
                "categories": categories
            },
        }
        return render(request, "home/create_collection.html", context)
    messages.warning(request, "you are not authorized to perform this action.")
    return redirect("home")


@login_required(login_url="login")
def delete_collecton(request, pk):
    uuid = UUID(pk)
    collection = Collection.objects.get(pk=uuid)
    seller = Seller.objects.get(username=request.user.username)
    if collection.seller == seller:
        collection.delete()
        if cache.get(pk):
            cache.delete(pk)
        messages.success(request, "Collection deleted")
    else:
        messages.error(request, "You are not authorized to perform this action.")
    return redirect("manage-collections")


@login_required(login_url="login")
def list_collections(request):
    is_logged_in = request.user.is_authenticated
    is_seller = get_is_seller(request)
    categories = Category.objects.all()
    collections = get_all_collections()
    data = []
    for collection in collections:
        data.append(
            {
                "item_count": collection.items.count(),
                "collection": collection,
            }
        )

    context = {
        "data": data,
        "user": {
            "is_logged_in": is_logged_in,
            "is_seller": is_seller,
            "categories": categories
        }
    }
    return render(request, "home/list_collections.html", context)


def view_collection(request, pk):
    try:
        is_logged_in = request.user.is_authenticated
        is_seller = get_is_seller(request)
        categories = Category.objects.all()
        uuid = UUID(pk)
        if cache.get(pk):
            collection = cache.get(pk)
        else:
            collection = Collection.objects.get(uuid=uuid)
            cache.set(pk, collection, 60*10)

        context = {
            "collection": collection,
            "user": {
                "is_logged_in": is_logged_in,
                "is_seller": is_seller,
                "categories": categories,
                "cart_total": get_cart_total(request)
            }
        }
        return render(request, "home/view_collection.html", context)
    except Exception as e:
        print(e)
        messages.error(request, "something went wrong.")
        return redirect("home")
