from django.contrib.auth.models import Group
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.meiduo_admin.serializer.admins import AdminSerializer
from apps.meiduo_admin.serializer.group import GroupSerializer
from apps.meiduo_admin.utils import PageNum
from apps.users.models import User


class AdminView(ModelViewSet):
    serializer_class = AdminSerializer

    queryset = User.objects.filter(is_staff=True)

    pagination_class = PageNum

    def groups(self, request):
        # 1、查询分组
        data = Group.objects.all()
        # 2、返回分组
        ser = GroupSerializer(data, many=True)
        return Response(ser.data)