from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse,HttpResponseBadRequest
from django.urls import reverse
from django.views import View
from apps.users.models import User

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
        from django.contrib.auth import login

        login(request,user)

        return redirect(reverse('contents:index'))
        return HttpResponse('OK')

class RegisterCountView(View):
    def get(self,request,username):
        count = User.objects.filter(username=username).count()

        return JsonResponse({'count':count})