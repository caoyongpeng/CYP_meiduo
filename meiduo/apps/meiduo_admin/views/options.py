from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.goods.models import SpecificationOption, SPUSpecification
from apps.meiduo_admin.serializer.options import OptionSerializer
from apps.meiduo_admin.utils import PageNum
from apps.meiduo_admin.serializer.Spec import SpecSerializer

class OptionView(ModelViewSet):
    serializer_class = OptionSerializer

    pagination_class = PageNum

    queryset = SpecificationOption.objects.all()

    def simple(self, request):
        # 1、查询规格表获取规格信息
        data = SPUSpecification.objects.all()
        # 2、序列化返回规格信息
        ser = SpecSerializer(data, many=True)
        return Response(ser.data)