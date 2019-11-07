from rest_framework import serializers
from apps.goods.models import SPUSpecification

class SpecSerializer(serializers.ModelSerializer):
    spu = serializers.StringRelatedField(read_only=True)
    spu_id = serializers.IntegerField()
    
    
    class Meta:
        
        model = SPUSpecification
        fields = '__all__'