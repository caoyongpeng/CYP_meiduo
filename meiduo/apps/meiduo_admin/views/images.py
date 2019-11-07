from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.meiduo_admin.utils import PageNum
from apps.goods.models import SKUImage, SKU
from apps.meiduo_admin.serializer.images import ImageSerializer, SKUImageSerializer


class ImageView(ModelViewSet):

    serializer_class = ImageSerializer

    queryset = SKUImage.objects.all()

    pagination_class = PageNum


    def simple(self,request):
        data = SKU.objects.all()

        ser = SKUImageSerializer(data,many=True)

        return Response(ser.data)