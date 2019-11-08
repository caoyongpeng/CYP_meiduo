from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.meiduo_admin.utils import PageNum
from apps.goods.models import SKU, SPU
from apps.meiduo_admin.serializer.SKUs import SKUSgoodsSerializer,CategorySerializer,SPUSpecSerializer
from apps.goods.models import GoodsCategory





class SKUsView(ModelViewSet):

    serializer_class =SKUSgoodsSerializer


    pagination_class = PageNum

    def get_queryset(self):

        keyword = self.request.query_params.get('keyword')

        if keyword == '' or keyword is None:
            return SKU.objects.all()
        else:
            return SKU.objects.filter(name__contains=keyword)

    def simple(self,request):

        data = GoodsCategory.objects.filter(subs=None)

        ser = CategorySerializer(data,many=True)

        return Response(ser.data)

    def specs(self,request,pk):

        spu = SPU.objects.get(id=pk)
        specs = spu.specs.all()
        ser = SPUSpecSerializer(specs,many=True)
        return Response(ser.data)

