from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.meiduo_admin.utils import PageNum
from apps.goods.models import SPUSpecification, SKU, SPU
from apps.meiduo_admin.serializer.Spec import SpecSerializer,SPUSerializer

class SpecView(ModelViewSet):

    serializer_class = SpecSerializer

    pagination_class = PageNum

    queryset = SPUSpecification.objects.all()


    def simple(self,request):
        data = SPU.objects.all()

        ser = SPUSerializer(data,many=True)

        return Response(ser.data)


