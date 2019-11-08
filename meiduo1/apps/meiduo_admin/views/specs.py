from rest_framework.viewsets import ModelViewSet
from apps.meiduo_admin.utils import PageNum
from apps.goods.models import SPUSpecification, SPU
from rest_framework.response import Response
from apps.meiduo_admin.serializer.specs import SpecSerializer,SPUSerializer


class SpecView(ModelViewSet):

    serializer_class = SpecSerializer

    queryset = SPUSpecification.objects.all()

    pagination_class = PageNum


    def simple(self,request):

        data = SPU.objects.all()

        ser = SPUSerializer(data,many=True)

        return Response(ser.data)