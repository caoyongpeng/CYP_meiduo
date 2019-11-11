from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.goods.models import GoodsChannel,GoodsChannelGroup,GoodsCategory
from apps.meiduo_admin.utils import PageNum
from apps.meiduo_admin.serializer.channels import ChannelSerizlizer,ChannelGroupSerializer,GoodsCateSerializer

class ChannelView(ModelViewSet):
    serializer_class = ChannelSerizlizer

    queryset = GoodsChannel.objects.all()

    pagination_class = PageNum


    def channel_types(self,request):
        data = GoodsChannelGroup.objects.all()
        ser = ChannelGroupSerializer(data,many=True)

        return Response(ser.data)

    def categories(self,request):
        data = GoodsCategory.objects.filter(subs=None)
        ser = GoodsCateSerializer(data,many=True)

        return Response(ser.data)
