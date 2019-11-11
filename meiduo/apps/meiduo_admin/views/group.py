from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import Group,Permission

from apps.meiduo_admin.serializer.group import GroupSerializer,PermissionGroupSerializer
from apps.meiduo_admin.utils import PageNum


class GroupView(ModelViewSet):

    serializer_class = GroupSerializer

    queryset = Group.objects.all()

    pagination_class = PageNum


    def simple(self,request):

        data = Permission.objects.all()
        ser = PermissionGroupSerializer(data,many=True)
        return Response(ser.data)