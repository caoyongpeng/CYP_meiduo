from django.contrib.auth.models import Permission,ContentType
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.meiduo_admin.serializer.permission import PermissionSerializer,ContentTypeSerializer
from apps.meiduo_admin.utils import PageNum


class PermissionView(ModelViewSet):

    serializer_class = PermissionSerializer

    queryset = Permission.objects.all()

    pagination_class = PageNum

    def content_types(self, request):
        content = ContentType.objects.all()
        ser = ContentTypeSerializer(content,many=True)
        return Response(ser.data)

