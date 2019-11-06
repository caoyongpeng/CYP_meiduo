from apps.goods.models import GoodsVisitCount

from rest_framework import serializers


class GoodsSerializer(serializers.ModelSerializer):

    category = serializers.StringRelatedField(read_only=True)
    class Meta:

        model = GoodsVisitCount

        fields = ('count','category')