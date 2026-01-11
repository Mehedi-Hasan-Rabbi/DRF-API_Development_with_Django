from django.http import JsonResponse
from api.serializers import ProductSerializer
from api.models import Product


# Create your views here.
def product_list(request):
    all_products = Product.objects.all()
    serializer = ProductSerializer(all_products, many=True)      # If we pass more than one product than many=False
    return JsonResponse({
        'data': serializer.data
    })