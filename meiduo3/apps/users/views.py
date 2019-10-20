import json
import re

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View
from django.http import HttpResponseBadRequest,HttpResponse,JsonResponse
from django.contrib.auth import login, authenticate,logout

from apps.users.models import User
from utils.response_code import RETCODE


class RegisterView(View):

    def get(self, request):

        return render(request, 'register.html')
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')

        if not all([username,password,password2,mobile]):
            return HttpResponseBadRequest('参数不全')

        if not re.match(r'[a-zA-Z0-9]{5,20}', username):
            return HttpResponseBadRequest('用户名不满足条件')

        if not re.match(r'[a-zA-Z0-9]{8,20}', password):
            return HttpResponseBadRequest('密码不符合规则')

        if password2 != password:
            return HttpResponseBadRequest('密码不一致')

        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseBadRequest('手机号错误')

        user = User.objects.create_user(username=username,password=password,mobile=mobile)

        login(request,user)

        response = redirect(reverse('contents:index'))

        response.set_cookie('username',user.username,max_age=3600)

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
        password = request.POST.get('pwd')
        remembered = request.POST.get('remembered')

        if not all([username, password]):
            return HttpResponseBadRequest('参数不全')
        user = authenticate(username=username, password=password)

        if user is None:
            return HttpResponseBadRequest('用户名或密码错误')
        login(request,user)

        if remembered == 'on':
            request.session.set_expiry(None)
        else:
            request.session.set_expiry(0)

        response = redirect(reverse('contents:index'))

        response.set_cookie('username', user.username, max_age=3600)

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

class EmailView(LoginRequiredMixin,View):
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
        from django.core.mail import send_mail

        # subject, message, from_email, recipient_list,
        # subject        主题
        subject = '美多商场激活邮件'
        # message,       内容
        message = ''
        # from_email,  谁发的
        from_email = '欢乐玩家<qi_rui_hua@163.com>'
        # recipient_list,  收件人列表
        recipient_list = ['13464604691@163.com']

        html_mesage = "<a href='http://www.huyouni.com'>戳我有惊喜</a>"

        send_mail(subject=subject,
                  message=message,
                  from_email=from_email,
                  recipient_list=recipient_list,
                  html_message=html_mesage)

        # ⑤ 返回相应
        return JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok'})