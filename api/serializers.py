from rest_framework import serializers
from .models import Product, Order, OrderItem, User


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'price',
            'stock',
        )

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError (
                "Price must be grater than 0."
            )
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            # 'order',
            'product',
            'quantity',
        )
      

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    # Calculated total price of the order
    total_price = serializers.SerializerMethodField()
    # This is working by 'get_total_price' function. 
    # It is default to use get_variable_name. 
    # Check DRF SerializerMethodField for more info.
    # If you want to use custom name then you can pass 'method_name' argument in SerializerMethodField.

    def get_total_price(self, obj):     # Here object is refering to Order
        order_items = obj.items.all()   # We have defined related_name='items' in OrderItem model.
        return sum(order_item.item_subtotal for order_item in order_items)

    class Meta:
        model = Order
        fields = (
            'order_id',
            'user',
            'created_at',
            'status',
            'items',
            'total_price',
        )
