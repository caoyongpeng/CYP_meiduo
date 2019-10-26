import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from django_redis import get_redis_connection

from apps.goods.models import SKU
from utils.response_code import RETCODE


class CartsView(View):
    def post(self,request):
        data = json.loads(request.body.decode())
        sku_id = data.get('sku_id')
        count = data.get('count')
        if not all([sku_id,count]):
            return JsonResponse({'code':RETCODE.PARAMERR,'errmsg':'参数不全'})
        try:
            sku=SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return JsonResponse({'code':RETCODE.NODATAERR,'errmsg':'没有次商品'})

        try:
            count = int(count)
        except Exception:
            return JsonResponse({'code':RETCODE.PARAMERR,'errmsg':"参数错误"})
        selected = True

        user = request.user

        if user.is_authenticated:
            redis_conn = get_redis_connection('carts')

            redis_conn.hset('cart_%s'%user.id,sku_id,count)

            redis_conn.sadd('selected_%s'%user.id,sku_id)

            return JsonResponse({'code':RETCODE.OK,'errmsg':'ok'})