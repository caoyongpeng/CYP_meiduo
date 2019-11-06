from rest_framework.views import APIView
from apps.users.models import User
from rest_framework.response import Response
from datetime import date,timedelta
from apps.goods.models import GoodsVisitCount
from apps.meiduo_admin.GoodsModelSerializer import GoodsSerializer

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
class UserCountView(APIView):
    def get(self,request):

        now_date = date.today()

        count = User.objects.filter(is_staff=False,last_login__gte=now_date).count()

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

class UserMouthCountView(APIView):
    def get(self,request):

        now_date = date.today()

        old_date = now_date - timedelta(30)

        date_list = []

        for i in range(30):

            index_date = old_date + timedelta(i)

            next_date = old_date + timedelta(i+1)

            count = User.objects.filter(is_staff=False,date_joined__gte=index_date,date_joined__lt=next_date).count()

            date_list.append({
                'count':count,
                'date':index_date
            })

        return Response(date_list)

class UserGoodsDayView(APIView):
    def get(self,request):

        now_date = date.today()

        data = GoodsVisitCount.objects.filter(date=now_date)

        ser = GoodsSerializer(data,many=True)

        return Response(ser.data)

