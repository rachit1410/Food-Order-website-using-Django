from django.contrib import admin

from home.models import (
    Category,
    Brand,
    Images,
    Item,
    Reviews,
    Status,
    CustomerOrder,
    VariantItem,
    Collection,
    Cart,
    CartItem,
    WishList,
    WishlistItems
)


admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Images)
admin.site.register(Item)
admin.site.register(Reviews)
admin.site.register(Status)
admin.site.register(CustomerOrder)
admin.site.register(VariantItem)
admin.site.register(Collection)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(WishList)
admin.site.register(WishlistItems)
