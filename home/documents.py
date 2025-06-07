from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from home.models import Item


@registry.register_document
class ItemDocument(Document):
    item_name = fields.TextField(
        fields={
            "keyword": fields.KeywordField(),
        }
    )
    item_description = fields.TextField(
        fields={
            "keyword": fields.KeywordField(),
        }
    )
    item_subcategory = fields.ObjectField(
        properties={
            'sub_catagory_name': fields.KeywordField(),
            'category': fields.ObjectField(properties={
                'category': fields.KeywordField(),
            }),
        },
        attr='item_subcategory'
    )

    item_brand = fields.ObjectField(
        properties={
            'brand': fields.KeywordField(),
        },
        attr='item_brand'
    )

    item_image = fields.ObjectField(
        properties={
            "image": fields.FileField()
        },
        attr="item_image"
    )

    seller = fields.ObjectField(
        properties={
            "username": fields.KeywordField()
        },
        attr="seller"
    )

    class Index:
        name = 'items'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Item
        fields = [
            "item_price",
            "item_discount_percentage",
            "rating",
            "quantity",
            "uuid"
        ]

    def prepare_item_subcategory(self, instance):
        subcat = instance.item_subcategory
        if not subcat:
            return {}
        return {
            "sub_catagory_name": subcat.sub_catagory_name,
            "category": {
                "category": subcat.category.category
            }
        }

    def prepare_item_brand(self, instance):
        brand = instance.item_brand
        if not brand:
            return {}
        return {
            "brand": brand.brand
        }

    def prepare_item_image(self, instance):
        image = instance.item_image
        if not image:
            return {}
        return {
            "image": image.image.url
        }
