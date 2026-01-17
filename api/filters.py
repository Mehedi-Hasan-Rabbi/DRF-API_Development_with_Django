import django_filters

from api.models import Product, Order

from rest_framework import filters

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['exact', 'iexact', 'contains', 'icontains'], 
            'price': ['exact', 'lt', 'gt', 'range'],
        }


class OrderFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(field_name='created_at__date')   # Extracts the date part from the DateTimeField and Ignores time (HH:MM:SS)
    class Meta:
        model = Order
        fields = {
            'status': ['exact'],
            'created_at': ['lt', 'gt', 'exact']
        }


class InStockFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)