from django.shortcuts import get_object_or_404

from api.serializers import ProductSerializer, OrderSerializer
from api.models import Product, Order, OrderItem

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


@api_view(['GET'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(['GET'])
def order_list(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)