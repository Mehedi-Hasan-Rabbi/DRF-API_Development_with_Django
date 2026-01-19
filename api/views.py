import time

from django.shortcuts import get_object_or_404
from django.db.models import Max
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.utils.decorators import method_decorator

from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer, OrderCreateSerializer, UserSerializer
from api.models import Product, Order, OrderItem, User
from api.filters import ProductFilter, InStockFilterBackend, OrderFilter

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework import viewsets
from rest_framework.throttling import ScopedRateThrottle

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
    # queryset = Product.objects.all('pk')
    throttle_classes = 'product'                    # Custom throttle scope for this view only
    throttle_classes = [ScopedRateThrottle]
    queryset = Product.objects.order_by('pk')       # While Specific class pagination it is better to use objects.order_by.
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
    search_fields = ['=name', 'description']            # Search for exact name. Search for partial description
    ordering_fields = ['name', 'price', 'stock']
    """
    DRF use only one pagination style at a time
    """
    # Examle 1 pagination style 
    # pagination_class = PageNumberPagination           # Apply pagination's page size = 2 only for product GET requests
    # pagination_class.page_size = 2

    # pagination_class.page_query_param = 'page_num'    # Instead of ?page int he URL it will show ?page_size
    # pagination_class.page_size_query_param = 'size'   # User can set page size in URL e.g. ?size=10
    # pagination_class.max_page_size = 10               # I using give higher than 10 it will take 10. Sometime user can mess it up.

    # Example 2 pagination style
    pagination_class = None


    """
    These two components (method_decorator, get_queryset) work together to optimize performance
    So, for learning purpose we are delaying for 2  second for first request. 
    In the second response the first response will be cached and second time response will be load from the cache.
    """
    @method_decorator(cache_page(60 * 60 * 2, key_prefix='product_list'))          # Cache data for (60 sec * 60) = 3600 sec = 1 Hour. (1 * 2) = 2 Hour      
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


    def get_queryset(self):
        time.sleep(2)
        return super().get_queryset()


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


# GET, PUT/PATCH, DELETE (No POST request)
class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_url_kwarg = 'product_id'       # See avobe class for more details

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


# class OrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items__product')   # Prefetching realeted information to reduce query
#     serializer_class = OrderSerializer


# class UserOrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items__product')   # Prefetching realeted information to reduce query
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         qs = super().get_queryset()
#         return qs.filter(user=user)

# Converting Orders generic view to viewset
class OrderViewSet(viewsets.ModelViewSet):          # All RESTful request is accepting
    throttle_classes = 'orders'
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None                         # To get rid of pagination even pagination is globally set

    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]


    @method_decorator(cache_page(60 * 15, key_prefix='order_list'))
    @method_decorator(vary_on_headers("Authorization"))                 # Cache will be different for different users based on Authorization header
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        # Can also check POST (self.request.method == 'POST')
        if self.action == 'create' or self.action == 'update':                 # If giving a POST request to create something then use OrderCreateSerializer
            return OrderCreateSerializer
        return super().get_serializer_class()       # Otherwise use assigned serializer. [serializer_class = OrderSerializer]


    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs

    @action(detail=False, methods=['get'], url_path='user-orders')      # If we want we can specify this action's permission by adding permission_class=[]
    def user_orders(self, request):
        orders = self.get_queryset().filter(user=request.user)
        serilizer = self.get_serializer(orders, many=True)
        return Response(serilizer.data)


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


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None
