from datetime import date

from rest_framework.views import APIView
from apps.users.models import User
from rest_framework.response import Response


class UserTotalCountView(APIView):
    def get(self,request):

        count = User.objects.filter(is_staff=False).count()

        return Response({
            'count':count
        })

class UserDayCountView(APIView):
    def get(self,request):

        now_date = date.today()

        count = User.objects.filter(is_staff=False,date_joined__gte=now_date).count()

        return Response({
            'count':count
        })

class UserOrderCountView(APIView):
    def get(self,request):

        now_date = date.today()
        users = set(User.objects.filter(is_staff=False,orderinfo__create_time__gte=now_date))

        count = len(users)

        return Response({
            'count':count
        })