from django.shortcuts import get_object_or_404
from django.db.models import Max

from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from api.models import Product, Order, OrderItem

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics


# Create your views here.
# @api_view(['GET'])
# def product_list(request):
#     all_products = Product.objects.all()
#     serializer = ProductSerializer(all_products, many=True)      # If we pass more than one product than many=False
#     # return Response({'data': serializer.data})
#     # or,
#     return Response(serializer.data)


# @api_view(['GET'])
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)


# @api_view(['GET'])
# def order_list(request):
#     orders = Order.objects.prefetch_related('items__product')   # Prefetching realeted information to reduce query
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)


# Converting avobe function based view to class based view using generics
class ProductListAPIView(generics.ListAPIView):         # Used for read-only endpoints to represent a collection of model instances.
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailAPIView(generics.RetrieveAPIView):   # Used for read-only endpoints to represent a single model instance.
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # If the urls.py file we use other than pk (e.g. product_id) we need a lookup_url_kwarg
    # lookup_url_kwarg = 'product_id'


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')   # Prefetching realeted information to reduce query
    serializer_class = OrderSerializer


@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        'product': products,
        'count': len(products),
        'max_price': products.aaggregate(max_price=Max('price'))['max_price']
    })
    return Response(serializer.data)
