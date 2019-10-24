from django.shortcuts import render
from django.core.cache import cache
# Create your views here.
from django.views import View
from django.http import JsonResponse
from apps.areas.models import Area
from utils.response_code import RETCODE


class AreasView(View):

    def get(self,request):
        parent_id = request.GET.get('area_id')
        if parent_id is None:
            cache_pro = cache.get('cache_pro')
            if cache_pro is None:
                proviences = Area.objects.filter(parent=None)
                cache_pro = []
                for pro in proviences:
                    cache_pro.append({
                        'id':pro.id,
                        'name':pro.name
                    })
                cache.set('cache_pro',cache_pro,3600)
            return JsonResponse({'code':RETCODE.OK,'province_list':cache_pro})
        else:
            city_list = cache.get(parent_id)
            if city_list is None:
                cities = Area.objects.filter(parent_id=parent_id)
                city_list = []
                for city in cities:
                    city_list.append({
                        'id':city.id,
                        'name':city.name
                    })
                cache.set(parent_id,city_list,3600)
            return JsonResponse({'code': RETCODE.OK, 'subs': city_list})