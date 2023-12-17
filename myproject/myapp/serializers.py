from rest_framework import serializers
from .models import OrderHeader, Product, Party, OrderItem, Person

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = '__all__'

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product_id', 'item_description', 'quantity', 'unit_amount']
        

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    customer_details = PersonSerializer(source='customer_party', read_only=True)
    #credit_card = serializers.SerializerMethodField()

    class Meta:
        model = OrderHeader
        fields = ['ORDER_ID', 'ORDER_NAME', 'PLACED_DATE', 'APPROVED_DATE', 'STATUS_ID', 'CURRENCY_UOM_ID', 'PRODUCT_STORE_ID', 'SALES_CHANNEL_ENUM_ID', 'GRAND_TOTAL', 'COMPLETED_DATE', 'order_items', 'customer_details']

    def get_credit_card(self, obj):
        return obj.get_credit_card()
