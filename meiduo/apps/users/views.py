import json

import re

from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.middleware import http
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.contrib.auth import login,logout
from django_redis import get_redis_connection

from apps.goods.models import SKU
from apps.users.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.users.utils import check_active_token
from celery_tasks.email.tasks import send_active_email
from utils.response_code import RETCODE


class RegisterView(View):
    def get(self,request):
        return render(request, 'register.html')

    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')

        if not all([username,password,password2,mobile]):
            return HttpResponseBadRequest('参数不全')
        import re

        if not re.match(r'[a-zA-Z0-9]{5,20}',username):
            return HttpResponseBadRequest('用户名错误')
        if not re.match(r'[a-zA-Z0-9]{8,20}', password):
            return HttpResponseBadRequest('密码不符合规则')
        if password2 != password:
            return HttpResponseBadRequest('密码不一致')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseBadRequest('手机号错误')

        user = User.objects.create_user(username=username,password=password,mobile=mobile)

        login(request, user)

        response = redirect(reverse('contents:index'))
        response.set_cookie('username', user.username, max_age=3600)
        return response
class RegisterCountView(View):
    def get(self,request,username):
        count=User.objects.filter(username=username).count()
        return JsonResponse({'count':count})

class LoginView(View):
    def get(self,request):
        return render(request,'login.html')
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        remembered = request.POST.get('remembered')

        if not all([username,password]):
            return HttpResponseBadRequest('参数不全')
        user = authenticate(username=username,password=password)

        if user is None:
            return HttpResponseBadRequest('用户名或密码错误')
        login(request,user)

        if remembered == 'on':
            request.session.set_expiry(None)
        else:
            request.session.set_expiry(0)

        response = redirect(reverse('contents:index'))

        response.set_cookie('username',user.username,max_age=3600)

        return response

class LogoutView(View):
    def get(self,request):
        logout(request)

        response = redirect(reverse('contents:index'))
        response.delete_cookie('username')
        return response

class UserCenterInfoView(LoginRequiredMixin,View):
    def get(self,request):
        # if request.user.is_authenticated:
        #     return render(request, 'user_center_info.html')
        # else:
        #     return redirect(reverse('users:login'))

        context = {
            'username': request.user.username,
            'mobile': request.user.mobile,
            'email': request.user.email,
            'email_active': request.user.email_active,
        }

        return render(request,'user_center_info.html',context=context)

class EmailView(View):
    def put(self,request):
        body = request.body
        body_str = body.decode()
        data = json.loads(body_str)
        # ② 验证
        email = data.get('email')
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return JsonResponse({'code': RETCODE.PARAMERR, 'errmsg': '邮箱不符合规则'})
        # ③ 更新数据
        request.user.email = email
        request.user.save()
        # ④ 给邮箱发送激活连接
        # from django.core.mail import send_mail
        #
        # # subject, message, from_email, recipient_list,
        # # subject        主题
        # subject = '美多商场激活邮件'
        # # message,       内容
        # message = ''
        # # from_email,  谁发的
        # from_email = '欢乐玩家<qi_rui_hua@163.com>'
        # # recipient_list,  收件人列表
        # recipient_list = ['qi_rui_hua@163.com']
        #
        # html_mesage = "<a href='http://www.huyouni.com'>戳我有惊喜</a>"
        #
        # send_mail(subject=subject,
        #           message=message,
        #           from_email=from_email,
        #           recipient_list=recipient_list,
        #           html_message=html_mesage)

        send_active_email.delay(request.user.id,email)
        # ⑤ 返回相应
        return JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok'})

class EmailActiveView(View):
    def get(self,request):
        token = request.GET.get('token')
        if token is None:
            return HttpResponseBadRequest('缺少参数')
        data = check_active_token(token)
        if data is None:
            return HttpResponseBadRequest('验证失败')
        id = data.get('id')
        email = data.get('email')
        try:
            user = User.objects.get(id=id,email=email)
        except User.DoesNotExist:
            return HttpResponseBadRequest('验证失败')
        else:
            user.email_active = True
            user.save()
        return redirect(reverse('users:center'))
class UserCenterSiteView(View):

    def get(self,request):

        return render(request,'user_center_site.html')

class ChangePasswordView(LoginRequiredMixin, View):

    def get(self, request):

        return render(request, 'user_center_pass.html')

    def post(self, request):

        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        new_password2 = request.POST.get('new_password2')

        if not all([old_password, new_password, new_password2]):
            return HttpResponseForbidden('缺少必传参数')
        if not re.match(r'^[0-9A-Za-z]{8,20}$', new_password):
            return HttpResponseBadRequest('密码最少8位，最长20位')
        if new_password != new_password2:
            return HttpResponseBadRequest('两次输入的密码不一致')

        if not request.user.check_password(old_password):
            return render(request, 'user_center_pass.html', {'origin_password_errmsg':'原始密码错误'})

        try:
            request.user.set_password(new_password)
            request.user.save()

        except Exception as e:
            import logging
            logger = logging.getLogger('django')
            logger.error(e)
            return render(request, 'user_center_pass.html', {'change_password_errmsg': '修改密码失败'})

        logout(request)

        response = redirect(reverse('users:login'))

        response.delete_cookie('username')

        return response
class UserHistoryView(LoginRequiredMixin,View):
    def post(self,request):
        user = request.user
        data = json.loads(request.body.decode())
        sku_id = data.get('sku_id')
        try:
            sku = SKU.objects.get(id = sku_id)
        except SKU.DoesNotExist:
            return JsonResponse({'code': RETCODE.NODATAERR, 'errmsg': '没有此商品'})
        redis_conn = get_redis_connection('history')

        redis_conn.lrem('history_%s'%user.id,0,sku_id)

        redis_conn.lpush('history_%s'%user.id,sku_id)

        redis_conn.ltrim('history_%s'%user,0,4)

        return JsonResponse({'code':RETCODE.OK,'errmsg':'ok'})