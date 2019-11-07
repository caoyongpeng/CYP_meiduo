from rest_framework import serializers
from apps.goods.models import SKUSpecification,SKU


class SKUSpecSerializer(serializers.ModelSerializer):
    spec_id = serializers.IntegerField(read_only=True)

    option_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = SKUSpecification

        fields = ('spec_id','option_id')
class SKUSgoodsSerializer(serializers.ModelSerializer):

    specs = SKUSpecSerializer(read_only=True,many=True)

    spu = serializers.StringRelatedField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)
    spu_id = serializers.IntegerField()
    category_id = serializers.IntegerField()

    class Meta:

        model = SKU
        fields = '__all__'
