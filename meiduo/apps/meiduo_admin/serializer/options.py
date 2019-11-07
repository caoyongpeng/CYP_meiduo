from rest_framework import serializers
from apps.goods.models import SpecificationOption

class OptionSerializer(serializers.ModelSerializer):
    spec = serializers.StringRelatedField(read_only=True)

    spec_id = serializers.IntegerField()
    class Meta:

        model=SpecificationOption

        fields = '__all__'