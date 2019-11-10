from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.meiduo_admin.serializer.orders import OrderSerializer
from apps.orders.models import OrderInfo
from apps.meiduo_admin.utils import PageNum


class OrderView(ModelViewSet):

    serializer_class = OrderSerializer

    queryset = OrderInfo.objects.all()

    pagination_class = PageNum

    def get_queryset(self):

        keyword = self.request.query_params.get('keyword')

        if keyword == '' or keyword is None:

            return OrderInfo.objects.all()
        else:
            return OrderInfo.objects.filter(user__username__contains=keyword)

    def status(self,request,order_id):

        order = OrderInfo.objects.get(order_id=order_id)

        status = request.data.get('status')

        order.status = status

        order.save()

        return Response({
            'order_id':order.order_id,
            'status':status
        })
