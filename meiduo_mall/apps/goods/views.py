from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from apps.contents.utils import get_categories
from apps.goods.models import GoodsCategory, SKU, GoodsVisitCount
from apps.goods.utils import get_breadcrumb
from utils.response_code import RETCODE


class ListView(View):
    def get(self,request,category_id,page):
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return render(request,'404.html')

        breadcrumb = get_breadcrumb(category)

        sort = request.GET.get('sort')
        if sort == 'default':
            order_field = 'create_time'
        elif sort == 'hot':
            order_field = 'sales'
        else:
            order_field = '-price'
        data = SKU.objects.filter(category=category)

        from django.core.paginator import Paginator

        paginator = Paginator(object_list=data,per_page=5)

        page_data = paginator.page(page)

        total_page = paginator.num_pages

        context = {

            'breadcrumb': breadcrumb,  # 面包屑导航
            'sort': sort,  # 排序字段
            'category': category,  # 第三级分类
            'page_skus': page_data,  # 分页后数据
            'total_page': total_page,  # 总页数
            'page_num': page,  # 当前页码
        }

        return render(request, 'list.html', context=context)
class HotSKUView(View):
    def get(self,request,category_id):
        try:
            category = GoodsCategory.objects.filter(id=category_id)
        except GoodsCategory.DoesNotExist:
            return JsonResponse({'code':RETCODE.NODATAERR,'errmsg':'没有此数据'})

        skus = SKU.objects.filter(category=category,is_launched=True)

        hot_skus = []
        for sku in skus:
            hot_skus.append({
                'id': sku.id,
                'default_image_url': sku.default_image.url,
                'name': sku.name,
                'price': sku.price
            })
        return JsonResponse({'code':RETCODE.OK,'errmsg':'ok',"hot_skus":hot_skus})

class DetailView(View):
    def get(self,request,sku_id):
        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return render(request,'404.html')
        categories = get_categories()

        breadcrumb = get_breadcrumb(sku.category)
        sku_specs = sku.specs.order_by('spec_id')
        sku_key = []
        for spec in sku_specs:
            sku_key.append(spec.option.id)

        skus = sku.spu.sku_set.all()

        spec_sku_map = {}
        for s in skus:

            s_specs = s.specs.order_by('spec_id')

            key = []
            for spec in s_specs:
                key.append(spec.option.id)

            spec_sku_map[tuple(key)] = s.id

        goods_specs = sku.spu.specs.order_by('id')

        if len(sku_key) < len(goods_specs):
            return
        for index, spec in enumerate(goods_specs):

            key = sku_key[:]

            spec_options = spec.options.all()
            for option in spec_options:

                key[index] = option.id
                option.sku_id = spec_sku_map.get(tuple(key))
            spec.spec_options = spec_options

        context = {
            'categories': categories,
            'breadcrumb': breadcrumb,
            'sku': sku,
            'specs': goods_specs,
        }

        return render(request, 'detail.html', context)
class VisitCountView(View):
    def post(self,request,category_id):
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return JsonResponse({'code':RETCODE.NODATAERR,'errmsg':'没有此分类'})
        from django.utils import timezone

        today = timezone.localdate()
        try:
            vc = GoodsVisitCount.objects.get(category=category,date=today)
        except GoodsVisitCount.DoesNotExist:
            GoodsVisitCount.objects.create(
                category=category,
                date=today,
                count=1
            )
            return JsonResponse({'code':RETCODE.OK,'errmsg':'ok'})
        else:
            vc.count+=1
            vc.save()
            return JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok'})