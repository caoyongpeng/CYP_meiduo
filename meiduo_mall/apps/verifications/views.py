from django.shortcuts import render
from django.http import HttpResponseBadRequest,HttpResponse,JsonResponse
# Create your views here.
from django.views import View
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection
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

        redis_text = redis_conn.get('img_%s'%image_code_id)

        if redis_text is None:
            return HttpResponseBadRequest('验证码过期')
        if redis_text.decode().lower() != image_code.lower():
            return HttpResponseBadRequest('验证码不一致')

        from random import randint
        sms_code = '%06d'%randint(0,999999)
        redis_conn.setex('sms_%s'%mobile,300,sms_code)
        from celery_tasks.sms.tasks import send_sms_code

        send_sms_code.delay(mobile,sms_code)
        return JsonResponse({'code':'0','msg':'ok'})