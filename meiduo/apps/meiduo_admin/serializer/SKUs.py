from rest_framework import serializers
from apps.goods.models import SKUSpecification, SKU, GoodsCategory, SPUSpecification, SpecificationOption


class SKUSpecSerializer(serializers.ModelSerializer):
    spec_id = serializers.IntegerField()

    option_id = serializers.IntegerField()

    class Meta:
        model = SKUSpecification

        fields = ('spec_id', 'option_id')


class SKUSgoodsSerializer(serializers.ModelSerializer):


    spu = serializers.StringRelatedField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)
    spu_id = serializers.IntegerField()
    category_id = serializers.IntegerField()
    specs = SKUSpecSerializer(many=True)
    class Meta:
        model = SKU
        fields = '__all__'

    def create(self, validated_data):
        specs = validated_data.get('specs')

        del validated_data['specs']
        sku = super().create(validated_data)
        for spec in specs:
            SKUSpecification.objects.create(sku=sku,spec_id=spec['spec_id'],option_id=spec['option_id'])
        return sku
    def update(self, instance, validated_data):
        specs = validated_data.get('specs')
        del validated_data['specs']
        sku = super().update(instance,validated_data)

        for spec in specs:
            SKUSpecification.objects.create(sku=sku,spec_id=spec['spec_id'],option_id=spec['option_id'])
        return sku



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory

        fields = '__all__'


class SPUSpecOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationOption
        fields = ('id', 'value')


class SPUSpecSerializer(serializers.ModelSerializer):
    options = SPUSpecOptionSerializer(many=True)
    spu = serializers.StringRelatedField(read_only=True)
    spu_id = serializers.IntegerField()

    class Meta:
        model = SPUSpecification
        fields = '__all__'
