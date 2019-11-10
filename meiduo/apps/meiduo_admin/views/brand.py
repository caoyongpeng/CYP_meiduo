from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.goods.models import Brand
from apps.meiduo_admin.utils import PageNum
from apps.meiduo_admin.serializer.brand import BrandSerializer
from fdfs_client.client import Fdfs_client


class BrandView(ModelViewSet):

    serializer_class = BrandSerializer

    queryset = Brand.objects.all()

    pagination_class = PageNum

    def create(self, request, *args, **kwargs):
        image = request.data.get('logo')
        name = request.data.get('name')
        first_letter = request.data.get('first_letter')
        if not all([image,name,first_letter]):
            return Response(status=400)
        client = Fdfs_client('/home/python/Desktop/CYP_meiduo/meiduo/utils/fastdfs/client.conf')
        res = client.upload_by_buffer(image.read())
        if res['Status'] != 'Upload successed.':
            return Response({"error": '上传失败'}, status=400)
        path = res.get('Remote file_id')

        # image_url = 'http://192.168.36.51:8888/' + path

        Brand.objects.create(name=name,first_letter=first_letter,logo=path)
        return Response(status=201)

    def update(self, request, *args, **kwargs):
        image = request.data.get('logo')
        name = request.data.get('name')
        first_letter = request.data.get('first_letter')
        if not all([image,name,first_letter]):
            return Response(status=400)
        client = Fdfs_client('/home/python/Desktop/CYP_meiduo/meiduo/utils/fastdfs/client.conf')
        res = client.upload_by_buffer(image.read())
        if res['Status'] != 'Upload successed.':
            return Response({"error": '上传失败'}, status=400)
        path = res.get('Remote file_id')
        brand = self.get_object()

        Brand.objects.filter(name=brand.name).update(logo=path,name=name,first_letter=first_letter)
        return Response(status=201)



