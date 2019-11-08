from rest_framework import serializers
from apps.goods.models import SKUImage, SKU
from fdfs_client.client import Fdfs_client



from script.generic_detail_html import generate_static_sku_detail_html


class ImageSerializer(serializers.ModelSerializer):


    class Meta:
        model = SKUImage
        fields = '__all__'


    def create(self, validated_data):
        sku = validated_data['sku']
        image = validated_data['image']
        client = Fdfs_client('/home/python/Desktop/CYP_meiduo/meiduo/utils/fastdfs/client.conf')
        res = client.upload_by_buffer(image.read())
        if res['Status'] != 'Upload successed.':
            raise serializers.ValidationError('上传失败')
        path = res.get('Remote file_id')

        img = SKUImage.objects.create(sku=sku,image=path)

        return img
    def update(self, instance, validated_data):
        sku = validated_data['sku']
        image = validated_data['image']
        client = Fdfs_client('/home/python/Desktop/CYP_meiduo/meiduo/utils/fastdfs/client.conf')
        res = client.upload_by_buffer(image.read())
        if res['Status'] != 'Upload successed.':
            raise serializers.ValidationError('上传失败')
        path = res.get('Remote file_id')

        instance.image = path

        instance.save()
        generate_static_sku_detail_html(sku.id)
        return instance



class SKUImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = SKU
        fields = '__all__'