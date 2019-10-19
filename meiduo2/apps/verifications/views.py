from django.shortcuts import render

# Create your views here.
from django.views import View
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from django.http import HttpResponse,HttpResponseBadRequest,JsonResponse
from random import randint
from libs.yuntongxun.sms import CCP

class ImageCodeView(View):
    def get(self,request,uuid):
        text,image = captcha.generate_captcha()
        redis_conn = get_redis_connection('code')

        redis_conn.setex('img_%s'%uuid,120,text)

        return HttpResponse(image,content_type='image/jpeg')
class SmsCodeView(View):
    def get(self,request,mobile):
        image_code = request.GET.get('image_code')
        image_code_id = request.GET.get('image_code_id')

        if not all([image_code,image_code_id]):
            return HttpResponseBadRequest('参数不全')

        redis_conn = get_redis_connection('code')

        redis_test = redis_conn.get('img_%s'%image_code_id)
        if redis_test is None:
            return HttpResponseBadRequest('图片验证码已过期')
        if redis_test.decode().lower() != image_code.lower():
            return HttpResponseBadRequest('图片验证码错误')

        sms_code = '%06d'%randint(0,999999)

        redis_conn.setex('sms_%s'%mobile,300,sms_code)

        from celery_tasks.sms.tasks import send_sms_code
        send_sms_code.delay(mobile,sms_code)

        # CCP().send_template_sms(mobile,[sms_code,5],1)

        return JsonResponse({'msg':'ok','code':'0'})
