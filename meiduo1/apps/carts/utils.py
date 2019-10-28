import base64
import pickle

from django_redis import get_redis_connection


def merge_cart_cookie_to_redis(request, user, response):

    cookie_str = request.COOKIES.get('carts')

    if cookie_str is None:
        return response
    else:
        carts = pickle.loads(base64.b64decode(cookie_str))

        redis_conn = get_redis_connection('carts')

        id_count_bytes = redis_conn.hgetall('carts_%s' % user.id)

        selected_ids = redis_conn.smembers('selected_%s' % user.id)

        id_count_redis = {}

        for id,count in id_count_bytes.items():
            id_count_redis[int(id)] = int(count)

        cookie_dict = {}

        selected_ids = []

        remove_selected_ids = []

        for sku_id,count_selected_dict in carts.items():
            cookie_dict[sku_id] = count_selected_dict['count']


            if count_selected_dict['selected']:

                selected_ids.append(sku_id)
            else:

                remove_selected_ids.append(sku_id)
        redis_conn.hmset('carts_%s'%user.id,cookie_dict)

        # redis_conn = get_redis_connection('carts')
        #
        # redis_conn.hmset('carts_%s' % user.id, cookie_dict)

        if len(selected_ids) > 0:
            redis_conn.sadd('selected_%s' % user.id, *selected_ids)

        if len(remove_selected_ids) > 0:
            redis_conn.srem('selected_%s' % user.id, *remove_selected_ids)

        response.delete_cookie('carts')
        return response