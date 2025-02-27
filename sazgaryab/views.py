from django.db import Error
from django.http import JsonResponse
from sazgaryab import services


def get_all_products(request):
    if request.method == 'GET':
        try:
            products = services.all_products()
        except Error as e:
            return JsonResponse({'error' : e.__str__()[8:len(e.__str__())-2]}, status=500)
        
        return JsonResponse({'products' : products}, status=200)
    return JsonResponse({"error" : 'Invalid request method'}, status=405)