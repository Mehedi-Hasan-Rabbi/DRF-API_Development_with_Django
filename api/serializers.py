from rest_framework import serializers
from .models import Product, Order, OrderItem, User


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            # 'id',
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
    # product = ProductSerializer()         # Show all the information from ProductSerializer()

    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        source='product.price'
    )

    class Meta:
        model = OrderItem
        fields = (
            # 'order',          # This will only show the PK.
            # 'product',        # Since this has an instantiation 'product = ProductSerializer()'. This will show according to serializer.

            'product_name',     # Only showing the field I want.
            'product_price',    # Only showing the field I want.
            'quantity',
            'item_subtotal',
        )


# Creating Nested Objects
class OrderCreateSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderItem
            fields = ('product', 'quantity')
    
    order_id = serializers.UUIDField(read_only=True)   
    items = OrderItemCreateSerializer(many=True)

    def update(self, instance, validated_data):
        orderitem_data = validated_data.pop('items')
        instance = super().update(instance, validated_data)
        
        if orderitem_data is not None:
            # Clear existing items (optional, depends on requirements)
            instance.items.all().delete()

            # Recreate items with the updated data
            for item in orderitem_data:
                OrderItem.objects.create(order=instance, **item)
        
        return instance

    def create(self, validated_data):
        orderitem_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item in orderitem_data:
            OrderItem.objects.create(order=order, **item)

        return order

    class Meta:
        model = Order
        fields = (
            'order_id',
            'user',
            'status',
            'items',
        )
        extra_kwargs = {
            'user': {'read_only': True}
        }


class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)        # id will be shown in GET but not in POST
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


class ProductInfoSerializer(serializers.Serializer):
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()
