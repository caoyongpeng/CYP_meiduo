from django.contrib.auth import login
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View
from django.http import HttpResponseBadRequest,HttpResponse

from apps.oauth.models import OAuthQQUser
from apps.oauth.utils import serect_openid, check_openid
from apps.users.models import User
from meiduo2 import settings
from QQLoginTool.QQtool import OAuthQQ







class QQLoginView(View):
    def get(self,request):
        code = request.GET.get('code')
        state = request.GET.get('state')
        if code is None:
            return HttpResponseBadRequest('code已过期')
        oauthqq = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                          client_secret=settings.QQ_CLIENT_SECRET,
                          redirect_uri=settings.QQ_REDIRECT_URI,
                          state=state)
        token = oauthqq.get_access_token(code)

        openid = oauthqq.get_open_id(token)

        try:
            qquser = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:

            new_openid = serect_openid(openid)

            return render(request, 'oauth_callback.html', context={'openid': new_openid})
        else:

            login(request, qquser.user)

            response = redirect(reverse('contents:index'))

            response.set_cookie('username', qquser.user.username, max_age=24 * 3600)

            return response

    def post(self, request):

        mobile = request.POST.get('mobile')
        pwd = request.POST.get('pwd')
        sms_code = request.POST.get('sms_code')
        secret_openid = request.POST.get('openid')

        # 添加解密
        openid = check_openid(secret_openid)
        if openid is None:
            return HttpResponseBadRequest('openid错误')

        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            #     如果不存在,说明用户手机号没有注册过,我们就以这个手机号注册一个用户
            user = User.objects.create_user(username=mobile,
                                            password=pwd,
                                            mobile=mobile)


        else:
            if not user.check_password(pwd):
                return HttpResponseBadRequest('密码错误')

        OAuthQQUser.objects.create(user=user, openid=openid)

        login(request, user)

        response = redirect(reverse('contents:index'))

        response.set_cookie('username', user.username, max_age=24 * 3600)

        return response