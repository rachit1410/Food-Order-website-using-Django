from django.http import JsonResponse
from home.documents import ItemDocument
from elasticsearch_dsl import Q

def search_for_collection(request):
    if request.method == "GET":
        searched = request.GET.get("q", "")
        if searched:
            search = ItemDocument.search()

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

