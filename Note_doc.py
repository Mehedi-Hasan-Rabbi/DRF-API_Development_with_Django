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
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

from django_filters.rest_framework import DjangoFilterBackend


# Source: https://www.django-rest-framework.org/api-guide/views/
############################ [ DRF views (Function Based) - Handle HTTP manually ] ############################
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


# @api_view(['GET'])
# def product_info(request):
#     products = Product.objects.all()
#     serializer = ProductInfoSerializer({
#         'product': products,
#         'count': len(products),
#         'max_price': products.aaggregate(max_price=Max('price'))['max_price']
#     })
#     return Response(serializer.data)


############################ [ DRF views (Class Based: APIView) - Handle HTTP manually ] ############################
# Example: Class based of product_info
# class ProductInfoAPIView(APIView):
#     def get(self, request):
#         products = Product.objects.all()
#         serializer = ProductInfoSerializer({
#             'products': products,
#             'count': len(products),
#             'max_price': products.aggregate(max_price=Max('price'))['max_price']
#         })
#         return Response(serializer.data)

"""
Note (DRF views both function and class based): 
    1. It is always batter to use class-based view.
    2. DRF views is just a DRFs version of Djangos View
    3. You handle HTTP methods manually
"""

# Source: https://www.django-rest-framework.org/api-guide/generic-views/
############################ [ DRF GenericAPIviews - Handle HTTP manually ] ############################
# Example: Haven't use this in the file. Just for example purpose.
# from rest_framework.generics import GenericAPIView
# class ProductAPIView(GenericAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


"""
Note: 
    1. Extends APIView
    2. Adds queryset & serializer support
"""

############################ [ DRF Genericviews - Handle HTTP automatically ] ############################
# class ProductListAPIView(generics.ListAPIView):           # Only GET: Used for read-only endpoints to represent a collection of model instances.
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


# class ProductDetailAPIView(generics.RetrieveAPIView):     # Only GET: Used for read-only endpoints to represent a single model instance.
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     # If the urls.py file we use other than pk (e.g. product_id) we need a lookup_url_kwarg
#     # lookup_url_kwarg = 'product_id'


# class OrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items__product')   # Prefetching realeted information to reduce query
#     serializer_class = OrderSerializer


# class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):              # GET, PUT, PATCH, DELETE (No POST request)
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     # lookup_url_kwarg = 'product_id'       # See avobe class for more details

#     def get_permissions(self):
#         self.permission_classes = [AllowAny]
#         if self.request.method in ['PUT', 'PATCH', 'DELETE']:
#             self.permission_classes = [IsAdminUser]
#         return super().get_permissions()


# class UserOrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items__product')   # Prefetching realeted information to reduce query
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         qs = super().get_queryset()
#         return qs.filter(user=user)


# class ProductCreateAPIView(generics.CreateAPIView):       # Only POST
#     model = Product
#     serializer_class = ProductSerializer
#     def create(self, request, *args, **kwargs):
#         print(request.data)
#         return super().create(request, *args, **kwargs)


# class ProductListCreatAPIView(generics.ListCreateAPIView):  # GET, POST: ListAPIView + CreateAPIView
#     # queryset = Product.objects.all('pk')
#     queryset = Product.objects.order_by('pk')       # While Specific class pagination it is better to use objects.order_by.
#     serializer_class = ProductSerializer
#     filterset_class = ProductFilter
#     """
#     Search Filter (?search='') is from rest_framework's filters [e.g. /?search='sion']
#     Django Filter (?parameter='') is from Django Filters        [e.g. /?name='water']
#     To use Django Filter 'filterset_class = ProductFilter' is enough
#     To use Search Filter (
#         from rest_framework import filters
#         filter_backends = [filters]
#         search_fields = ['name', 'description']
#     )
#     To Use BOTH (
#         from rest_framework import filters
#         from django_filters.rest_framework import DjangoFilterBackend
#         filter_backends = [filters, DjangoFilterBackend]
#         search_fields = ['name', 'description']
#     )
#     """ 
#     filter_backends = [
#         DjangoFilterBackend, 
#         filters.SearchFilter, 
#         filters.OrderingFilter,
#         InStockFilterBackend,
#     ]
#     search_fields = ['=name', 'description']        # Search for exact name. Search for partial description
#     ordering_fields = ['name', 'price', 'stock']
#     """
#     DRF use only one pagination style at a time
#     """
#     # Examle 1 pagination style:
#         # pagination_class = PageNumberPagination         # Apply pagination's page size = 2 only for product GET requests
#         # pagination_class.page_size = 2
#         # pagination_class.page_query_param = 'page_num'  # Instead of ?page int he URL it will show ?page_size
#         # pagination_class.page_size_query_param = 'size' # User can set page size in URL e.g. ?size=10
#         # pagination_class.max_page_size = 10             # I using give higher than 10 it will take 10. Sometime user can mess it up.
#     # Example 2 pagination style:
#     pagination_class = LimitOffsetPagination
#     def get_permissions(self):
#         self.permission_classes = [AllowAny]
#         if self.request.method == 'POST':
#             self.permission_classes = [IsAdminUser]
#         return super().get_permissions()

