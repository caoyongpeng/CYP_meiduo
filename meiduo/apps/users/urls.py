from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^register/$',views.RegisterView.as_view(),name='register'),
    url(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/$',views.RegisterCountView.as_view()),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^center/$',views.UserCenterInfoView.as_view(),name='center'),
    url(r'^emails/$', views.EmailView.as_view(), name='email'),
    url(r'^emailsactive/$', views.EmailActiveView.as_view(), name='emailactive'),
    url(r'^site/$', views.UserCenterSiteView.as_view(), name='site'),
    url(r'^pwd/$', views.ChangePasswordView.as_view(), name='pwd'),
    url(r'^browse_histories/$', views.UserHistoryView.as_view(), name='history'),
    url(r'^addresses/create/$', views.CreateAddressView.as_view(), name='createaddress'),
    url(r'^addresses/$', views.AddressView.as_view(), name='address'),
    url(r'^addresses/(?P<address_id>\d+)/$', views.UpdateDestroyAddressView.as_view(), name='addressesupdate'),
    url(r'^find_password/$', views.FindPwdView.as_view(),name='findpwd'),
    url(r'^users/(?P<user_id>\d+)/password/$', views.ChangePwdView.as_view()),

]