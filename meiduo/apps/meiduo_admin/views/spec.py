from rest_framework.viewsets import ModelViewSet
from apps.meiduo_admin.utils import PageNum
from apps.goods.models import SPUSpecification
from apps.meiduo_admin.serializer.Spec import SpecSerializer

class SpecView(ModelViewSet):
    
    serializer_class = SpecSerializer
    
    pagination_class = PageNum
    
    queryset = SPUSpecification.objects.all()



