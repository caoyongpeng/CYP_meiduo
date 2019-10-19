from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse,HttpResponseBadRequest
from django.urls import reverse
from django.views import View
from apps.users.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout
from django.contrib.auth.mixins import LoginRequiredMixin

class RegisterView(View):
    def get(self,request):
        return render(request,'register.html')
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')

        if not all([username,password,password2,mobile]):
            return HttpResponseBadRequest('参数不全')
        import re

        if not re.match(r'[a-zA-Z0-9]{5,20}', username):
            return HttpResponseBadRequest('用户名错误')
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
        count = User.objects.filter(username=username).count()

        return JsonResponse({'count':count})
class LoginView(View):
    def get(self,request):

        return render(request,'login.html')
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('pwd')
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
        return render(request,'user_center_info.html')
