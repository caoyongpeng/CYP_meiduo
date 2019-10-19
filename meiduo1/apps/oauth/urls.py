from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^oauth_callback/$', views.QQAuthUserView.as_view()),
]