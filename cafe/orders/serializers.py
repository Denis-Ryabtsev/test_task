from rest_framework import serializers

from orders.models import Order, OrderDetail


class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ['product_name']


class OrderSerializer(serializers.ModelSerializer):
    detail_order = OrderDetailsSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'table_number', 
            'detail_order', 
            'order_cost', 
            'order_status'
        ]
    