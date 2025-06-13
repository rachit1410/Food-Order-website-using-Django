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
    WishlistItems,
    MostSearched
)


class CollectionAdmin(admin.ModelAdmin):
    search_fields = ['collection_name', 'items__item_name', 'items__sku']
    list_display = ['collection_name', 'seller', 'collection_description']
    filter_horizontal = ['items']


admin.site.register(Collection, CollectionAdmin)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Images)
admin.site.register(Item)
admin.site.register(Reviews)
admin.site.register(Status)
admin.site.register(CustomerOrder)
admin.site.register(VariantItem)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(WishList)
admin.site.register(WishlistItems)
admin.site.register(MostSearched)
