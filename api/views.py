from django.http import JsonResponse

from api.serializers import ProductSerializer
from api.models import Product

from rest_framework.response import Response
from rest_framework.decorators import api_view


# Create your views here.
@api_view(['GET'])
def product_list(request):
    all_products = Product.objects.all()
    serializer = ProductSerializer(all_products, many=True)      # If we pass more than one product than many=False
    # return Response({'data': serializer.data})
    # or,
    return Response(serializer.data)
