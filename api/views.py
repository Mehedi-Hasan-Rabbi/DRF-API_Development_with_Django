from django.shortcuts import get_object_or_404
from django.db.models import Max

from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from api.models import Product, Order, OrderItem
from api.filters import ProductFilter, InStockFilterBackend

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination

from django_filters.rest_framework import DjangoFilterBackend


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
# class ProductListAPIView(generics.ListAPIView):         # Used for read-only endpoints to represent a collection of model instances.
#     # GET request
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


# class ProductCreateAPIView(generics.CreateAPIView):
#     # POST request
#     model = Product
#     serializer_class = ProductSerializer

#     def create(self, request, *args, **kwargs):
#         print(request.data)
#         return super().create(request, *args, **kwargs)

# Above two (ListAPIView + CreateAPIView) can be combined using ListCreateAPIView
class ProductListCreatAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter

    """
    Search Filter (?search='') is from rest_framework's filters [e.g. /?search='sion']
    Django Filter (?parameter='') is from Django Filters        [e.g. /?name='water']

    To use Django Filter 'filterset_class = ProductFilter' is enough
    To use Search Filter (
        from rest_framework import filters
        filter_backends = [filters]
        search_fields = ['name', 'description']
    )
    To Use BOTH (
        from rest_framework import filters
        from django_filters.rest_framework import DjangoFilterBackend
        filter_backends = [filters, DjangoFilterBackend]
        search_fields = ['name', 'description']
    )
    """ 

    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter, 
        filters.OrderingFilter,
        InStockFilterBackend,
    ]
    search_fields = ['=name', 'description']        # Search for exact name. Search for partial description
    ordering_fields = ['name', 'price', 'stock']
    pagination_class = PageNumberPagination         # Apply pagination's page size = 2 only for product GET requests
    pagination_class.page_size = 2

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

# # Only GET Action for single product
# class ProductDetailAPIView(generics.RetrieveAPIView):   # Used for read-only endpoints to represent a single model instance.
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     # If the urls.py file we use other than pk (e.g. product_id) we need a lookup_url_kwarg
#     # lookup_url_kwarg = 'product_id'


# GET, PUT, PATCH, DELETE
class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_url_kwarg = 'product_id'       # See avobe class for more details

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')   # Prefetching realeted information to reduce query
    serializer_class = OrderSerializer


class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')   # Prefetching realeted information to reduce query
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(user=user)


# @api_view(['GET'])
# def product_info(request):
#     products = Product.objects.all()
#     serializer = ProductInfoSerializer({
#         'product': products,
#         'count': len(products),
#         'max_price': products.aaggregate(max_price=Max('price'))['max_price']
#     })
#     return Response(serializer.data)

class ProductInfoAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': len(products),
            'max_price': products.aggregate(max_price=Max('price'))['max_price']
        })
        return Response(serializer.data)
