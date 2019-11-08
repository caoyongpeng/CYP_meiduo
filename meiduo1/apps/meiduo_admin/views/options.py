from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from apps.meiduo_admin.serializer.specs import SpecSerializer
from apps.meiduo_admin.utils import PageNum
from apps.goods.models import SpecificationOption, SPUSpecification
from apps.meiduo_admin.serializer.options import OptionsSerializer


class OptionsView(ModelViewSet):

    serializer_class = OptionsSerializer

    queryset = SpecificationOption.objects.all()

    pagination_class = PageNum


    def simple(self,request):

        data = SPUSpecification.objects.all()

        ser = SpecSerializer(data,many=True)

        return Response(ser.data)