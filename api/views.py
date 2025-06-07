from django.http import JsonResponse
from home.documents import ItemDocument
from elasticsearch_dsl import Q
from home.models import Cart, CartItem, Item, WishList, WishlistItems
from accounts.models import Customer
from uuid import UUID


def search_for_collection(request):
    if request.method == "GET":
        searched = request.GET.get("q", "")
        if searched:
            search = ItemDocument.search()

            search = search.query(
                Q(
                    "multi_match", query=searched, fields=[
                        "item_name",
                    ],
                    fuzziness="AUTO"
                )
            )

            total_items = search.count()
            results = search.execute()

            if total_items < 1:
                return JsonResponse({
                    "status": False,
                    "message": "no results found",
                    "data": {}
                })

            # Serialize results for JSON response
            items = []
            for hit in results:
                item = hit.to_dict()
                item['id'] = str(hit.meta.id)
                items.append(item)

            return JsonResponse({
                "status": True,
                "message": "items fetched",
                "data": {
                    "items": items,
                }
            })
        return JsonResponse({
            "status": False,
            "message": "search term not provided",
            "data": {}
        })


def add_to_cart(request):
    if request.method == "POST":
        try:
            item_id = request.POST.get("item_id")
            item_quantity = request.POST.get("item_quantity")
            customer = Customer.objects.filter(username=request.user.username)
            if not customer.exists():
                return JsonResponse({
                    "status": False,
                    "message": "you are not authorized to perform this action.",
                    "data": {}
                })
            uuid = UUID(item_id)
            item = Item.objects.get(uuid=uuid)

            cart = Cart.objects.get(customer=customer[0])

            if CartItem.objects.filter(
                item=item,
                cart=cart,
            ).exists():
                cart_item = CartItem.objects.get(item=item, cart=cart)
                cart_item.item_quantity = int(cart_item.item_quantity)+int(item_quantity)
                cart_item.save()
            else:
                CartItem.objects.create(
                    item=item,
                    cart=cart,
                    item_quantity=int(item_quantity)
                )

            return JsonResponse({
                "status": True,
                "message": "item added to cart",
                "data": {}
            })
        except Exception as e:
            print(e)
            return JsonResponse({
                "status": False,
                "message": "somehting went wrong",
                "data": {}
            })


def add_to_wishlist(request):
    if request.method == "POST":
        try:
            item_id = request.POST.get("item_id")
            customer = Customer.objects.filter(username=request.user.username)
            if not customer.exists():
                return JsonResponse({
                    "status": False,
                    "message": "you are not authorized to perform this action.",
                    "data": {}
                })
            uuid = UUID(item_id)
            item = Item.objects.get(uuid=uuid)

            wishlist = WishList.objects.get(customer=customer[0])

            if wishlistitem := WishlistItems.objects.filter(
                item=item,
                wishlist=wishlist,
            ):
                wishlistitem.delete()
                return JsonResponse({
                    "status": True,
                    "message": "item removed from wishlist",
                    "data": {}
                })
            else:
                WishlistItems.objects.create(
                    item=item,
                    wishlist=wishlist,
                )

                return JsonResponse({
                    "status": True,
                    "message": "item added to wishlist",
                    "data": {}
                })
        except Exception as e:
            print(e)
            return JsonResponse({
                "status": False,
                "message": "somehting went wrong",
                "data": {}
            })
