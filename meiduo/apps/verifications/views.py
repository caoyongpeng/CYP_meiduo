import json

from django.http import HttpResponse,HttpResponseBadRequest
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

from django.views import View
from django_redis import get_redis_connection
from meiduo import settings
from apps.users.models import User
from libs.yuntongxun.sms import CCP
from utils.response_code import RETCODE


class ImageCodeView(View):
    def get(self,request,uuid):
        from libs.captcha.captcha import captcha
        text,image = captcha.generate_captcha()
        from django_redis import get_redis_connection
        redis_conn = get_redis_connection('code')
        redis_conn.setex('img_%s'%uuid,120,text)
        return HttpResponse(image,content_type='image/jpeg')

class SmsCodeView(View):
    def get(self,request,mobile):

        image_code = request.GET.get('image_code')
        image_code_id = request.GET.get('image_code_id')

        if not all([image_code,image_code_id]):
            return HttpResponseBadRequest('参数不全')

        from django_redis import get_redis_connection

        redis_conn = get_redis_connection('code')

        redis_text = redis_conn.get('img_%s'%image_code_id)

        if redis_text is None:
            return HttpResponseBadRequest('图片验证码已过期')

        if redis_text.decode().lower() != image_code.lower():
            return HttpResponseBadRequest('图片验证码不一致')

        from random import randint
        sms_code = '%06d'%randint(0,999999)

        redis_conn.setex('sms_%s'%mobile,300,sms_code)
        # CCP().send_template_sms(mobile,[sms_code,5],1)
        from celery_tasks.sms.tasks import send_sms_code
        send_sms_code.delay(mobile,sms_code)

        return JsonResponse({'msg':'ok','code':'0'})
class PwdCodeView(View):
    def get(self,request,username):
        uuid = request.GET.get('image_code_id')
        image_code = request.GET.get('text')

        redis_conn = get_redis_connection('code')
        redis_image_code = redis_conn.get('img_%s'%uuid)

        if redis_image_code is None:
            return JsonResponse({'code':RETCODE.IMAGECODEERR,'errmsg':'图片验证码过期'})

        redis_conn.delete('img_%s'%uuid)

        if redis_image_code.decode().lower() != image_code.lower():
            return JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '图形验证码错误'})
        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({},status=404)

        json_str = json.dumps({"user_id":user.id,"mobile":user.mobile})

        return JsonResponse({'mobile': user.mobile, 'access_token': json_str})

class PwdSMSCodeView(View):
    def get(self,request):
        access_token = request.GET.get('access_token')

        user_dict = json.loads(access_token)

        if user_dict is None:
            return JsonResponse({},status=400)

        mobile = user_dict['mobile']

        try:
            User.objects.get(mobile=mobile)

        except:

            return JsonResponse({},status=400)
        redis_conn = get_redis_connection('code')

        if redis_conn.get('sms_%s'%mobile) is not None:
            return JsonResponse({'code':RETCODE.SMSCODERR,'errmsg':'发送短信太频繁'})

        from random import randint
        sms_code = '%06d'%randint(0,999999)

        redis_conn.setex('sms_%s'%mobile,300,sms_code)

        from celery_tasks.sms.tasks import send_sms_code

        send_sms_code.delay(mobile,sms_code)

        return JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})

class PwdCheckCodeView(View):
    def get(self,request,username):

        sms_code = request.GET.get('sms_code')

        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({},status=400)

        redis_conn = get_redis_connection('code')

        redis_sms_code = redis_conn.get('sms_%s'%user.mobile)

        if redis_sms_code is None:
            return HttpResponseForbidden('短信验证码过期')
        redis_conn.delete('sms_%s'%user.mobile)

        if redis_sms_code.decode().lower() != sms_code:
            return HttpResponseForbidden('验证码错误')
        json_str = json.dumps({"user_id": user.id, 'mobile': user.mobile})
        return JsonResponse({'user_id': user.id, 'access_token': json_str})





