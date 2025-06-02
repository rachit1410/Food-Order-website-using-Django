from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from home.utils import get_is_seller
from home.models import (Collection, Category, Brand, SubCategory)
from home.documents import ItemDocument
from elasticsearch_dsl import Q
from uuid import UUID


def home(request):
    is_seller = None
    is_logged_in = request.user.is_authenticated
    if is_logged_in:
        is_seller = get_is_seller(request)
    
    list_categories = Category.objects.all().order_by('category')
    
    context = {
        'is_logged_in': is_logged_in,
        'is_seller': is_seller,
        'query': {
            "categories": list_categories
        }
    }

    return render(request, "home/home.html", context)


def about_us(request):
    return render(request, "home/about_us.html")


def contact_us(request):
    return render(request, "home/contact_us.html")


def item_detail(request, pk):
    return render(request, "home/product_detail.html")


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
    sort_by = request.GET.get("sort", "item_name")

    search = ItemDocument.search()
    
    if searched:
        search = search.query(
            Q(
                "multi_match", query=searched, fields = [
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
    
    if category != "":
        search = search.filter("match", item_subcategory__category__category=category)
    
    if sub_cat!= "":
        search = search.filter("match", item_subcategory__sub_catagory_name=sub_cat)
        
    if brand!= "":
        search = search.filter("match", item_brand__brand=brand)
    
    if min_price!= "":
        search = search.filter("range", item_price={"gte": min_price})

    if max_price!= "":
        search = search.filter("range", item_price={"lte": max_price})

    
    if sort_by == "relevance" or not sort_by:
        search.sort("_score")
    else:
        if sort_by.startswith("-"):
            search = search.sort({sort_by[1:]: {"order": "desc"}})
        else:
            search = search.sort({sort_by: {"order": "asc"}})

    total_items = search.count()
    
    # pagination
    page_number = int(request.GET.get("page", 1))
    per_page = 30
    start = (page_number - 1) * per_page
    previous = page_number > 1
    next = start + per_page < search.count()

    search = search[start:start + per_page]

    results = search.execute()
    
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
        },
        "data": {
            "count": total_items,
            "products": results
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


def check_out(request):
    return render(request, "home/check_out.html")


def card_pay(request):
    return render(request, "home/card-pay.html")


def upi_pay(request):
    return render(request, "home/upi-pay.html")


def cart(request):
    return render(request, "home/cart.html")


def thank(request):
    return render(request, "home/thankyou.html")


def not_found(request):
    return render(request, "404.html")


@login_required(login_url="login")
def my_collections(request):
    if get_is_seller(request):
        collections = Collection.objects.filter(seller__id=request.user.id)
        context = {
            "collections": collections
        }
        return render(request, "home/list_my_collections.html", context)
    return redirect("home")

def create_collection(request):
    if get_is_seller(request):
        return render(request, "home/create_collection.html")
