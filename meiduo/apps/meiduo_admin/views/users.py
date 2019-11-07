from rest_framework.generics import ListCreateAPIView
from apps.meiduo_admin.serializer.Users import UserSerializer
from apps.users.models import User
from apps.meiduo_admin.utils import PageNum

class UsersView(ListCreateAPIView):

    serializer_class = UserSerializer

    queryset = User.objects.filter(is_staff=False)

    pagination_class = PageNum


    def get_queryset(self):

        keyword = self.request.query_params.get('keyword')

        if keyword == '' or keyword is None:

            return User.objects.filter(is_staff=False)
        else:

            return User.objects.filter(is_staff=False,username__contains=keyword)