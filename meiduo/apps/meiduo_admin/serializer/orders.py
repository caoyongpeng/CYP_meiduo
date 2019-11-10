from rest_framework import serializers

from apps.goods.models import SKU
from apps.orders.models import OrderInfo,OrderGoods

class SKUGoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = SKU
        fields = ('name','default_image')
class OrderGoodsSerializer(serializers.ModelSerializer):
    sku = SKUGoodSerializer(read_only=True)
    class Meta:
        model = OrderGoods
        fields = ('count','price','sku')

class OrderSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only=True)

    skus = OrderGoodsSerializer(many=True,read_only=True)
    class Meta:

        model = OrderInfo

        fields = '__all__'