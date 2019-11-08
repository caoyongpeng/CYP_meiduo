from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

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

