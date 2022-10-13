from rest_framework import serializers
from .models import *


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = "__all__"

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"

class CashSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cash
        fields = "__all__"

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

class QuitpriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quitprice
        fields = "__all__"

class QuitmoneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Quitmoney
        fields = "__all__"
