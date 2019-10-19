from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View
from django.http import HttpResponse,HttpResponseBadRequest
from QQLoginTool.QQtool import OAuthQQ
from meiduo1 import settings
from apps.oauth.models import OAuthQQUser
from django.contrib.auth import login

class QQAuthUserView(View):
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
            return render(request,'oauth_callback.html',context={'openid':openid})
        else:
            login(request,qquser.user)
            response = redirect(reverse('contents:index'))
            response.set_cookie('username',qquser.user.username,max_age=3600)
            return response

