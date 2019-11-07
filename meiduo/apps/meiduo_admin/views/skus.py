from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.meiduo_admin.utils import PageNum
from apps.goods.models import SKU
from apps.meiduo_admin.serializer.SKUs import SKUSgoodsSerializer,CategorySerializer
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

        data = GoodsCategory.objects.filter(parent_id__gt=37)

        ser = CategorySerializer(data,many=True)

        return Response(ser.data)