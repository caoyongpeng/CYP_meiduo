import base64
import json

from django.http import JsonResponse
from django.shortcuts import render
import base64
import pickle
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
            sku = SKU.objects.get(id = sku_id)
        except SKU.DoesNotExist:
            return JsonResponse({'code':RETCODE.NODATAERR,'errmsg':'没有此商品'})
        try:
            count = int(count)
        except Exception:
            return JsonResponse({'code':RETCODE.PARAMERR,'errmsg':"参数错误"})
        selected = True
        user = request.user

        if user.is_authenticated:
            redis_conn = get_redis_connection('carts')

            redis_conn.hset('carts_%s'%user.id,sku_id,count)

            redis_conn.sadd('selected_%s'%user.id,sku_id)

            return JsonResponse({'code':RETCODE.OK,'errmsg':'ok'})
        else:

            carts_str = request.COOKIES.get('carts')
            if carts_str is None:
                carts_data = {
                    sku_id:{'count':count,'selected':selected}
                }
            else:
                decode_data = base64.b64decode(carts_str)

                cookie_data = pickle.loads(decode_data)

                if sku_id in cookie_data:
                    origin_count = cookie_data[sku_id]['count']

                    count += origin_count

                    cookie_data[sku_id] = {'count':count,'selected':True}

                else:
                    cookie_data[sku_id] = {'count':count,'selected':True}
        cookie_bytes=pickle.dumps(cookie_data)

        cookie_str = base64.encode(cookie_bytes)

        response = JsonResponse({'code':RETCODE.OK,'errmsg':'ok'})

        response.set_cookie('carts', cookie_str, max_age=7 * 24 * 3600)

        return response

