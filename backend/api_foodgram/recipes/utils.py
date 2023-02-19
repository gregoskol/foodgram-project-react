from django.http import HttpResponse


def download_shopping_list(ingredients_list):
    shop_list = []
    for ingredient in ingredients_list:
        shop_list.append(
            f'{ingredient["ingredient__name"]} - {ingredient["amount"]} '
            f'{ingredient["ingredient__measurement_unit"]} \n'
        )

    response = HttpResponse(shop_list, "Content-Type: text/plain")
    response["Content-Disposition"] = "attachment; " 'filename="shoplist.txt"'
    return response
