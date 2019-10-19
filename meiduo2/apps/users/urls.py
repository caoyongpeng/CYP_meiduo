from django.conf.urls import url



# def text(request):
#     logger = logging.getLogger('django')
#     logger.debug('测试logging模块debug')
#     return HttpResponse('text')
from . import views

urlpatterns = [
    url(r'^register/$',views.RegisterView.as_view(),name='register'),
    url(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/$',views.RegisterCountView.as_view()),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^center/$',views.UserCenterInfoView.as_view(),name='center'),
]