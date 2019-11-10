from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from fdfs_client.client import Fdfs_client
from apps.goods.models import SPU,Brand,GoodsCategory
from apps.meiduo_admin.serializer.spus import SPUSerializer, BrandSerializer,  GoodsCategorySerializer
from apps.meiduo_admin.utils import PageNum



class SPUView(ModelViewSet):

    serializer_class = SPUSerializer

    pagination_class = PageNum

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')

        if keyword == '' or keyword is None:
            return SPU.objects.all()
        else:
            return SPU.objects.filter(name=keyword)


    def simple(self,request):

        data = Brand.objects.all()

        ser = BrandSerializer(data,many=True)

        return Response(ser.data)

    def channel(self,request):

        data = GoodsCategory.objects.filter(parent=None)


        ser = GoodsCategorySerializer(data,many=True)

        return Response(ser.data)
    def channels(self,request,pk):

        data = GoodsCategory.objects.filter(parent=pk)

        ser = GoodsCategorySerializer(data,many=True)

        return Response(ser.data)

    def images(self,request):
        image = request.data.get('image')
        client = Fdfs_client('/home/python/Desktop/CYP_meiduo/meiduo/utils/fastdfs/client.conf')
        res = client.upload_by_buffer(image.read())
        if res['Status'] != 'Upload successed.':
            return Response({"error": '上传失败'}, status=400)
        path = res.get('Remote file_id')

        image_url = 'http://192.168.36.51:8888/' + path
        return Response({'img_url':image_url})

