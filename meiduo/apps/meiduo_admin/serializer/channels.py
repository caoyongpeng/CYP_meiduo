from rest_framework import serializers
from apps.goods.models import GoodsChannel,GoodsChannelGroup,GoodsCategory

class ChannelGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodsChannelGroup
        fields = '__all__'

class ChannelSerizlizer(serializers.ModelSerializer):
    group = serializers.StringRelatedField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)
    group_id = serializers.IntegerField()
    category_id = serializers.IntegerField()

    class Meta:
        model = GoodsChannel
        fields = '__all__'

class GoodsCateSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodsCategory
        fields = '__all__'