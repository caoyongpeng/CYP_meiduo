
from django.conf.urls import url
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token
from .views import statistical,users
from . import views
from rest_framework.routers import DefaultRouter
from apps.meiduo_admin.views import spec,skus

urlpatterns = [
    url(r'^authorizations/$', obtain_jwt_token),
    url(r'^statistical/total_count/$',statistical.UserTotalCountView.as_view()),
    url(r'^statistical/day_increment/$',statistical.UserDayCountView.as_view() ),
    url(r'^statistical/day_orders/$',statistical.UserOrderCountView.as_view() ),
    url(r'^statistical/month_increment/$',statistical.UserMouthCountView.as_view() ),
    url(r'^statistical/day_active/$',statistical.UserCountView.as_view() ),
    url(r'^statistical/goods_day_views/$',statistical.UserGoodsDayView.as_view() ),
    url(r'^users/$',users.UsersView.as_view() ),
    url(r'^goods/simple/$',spec.SpecView.as_view({'get':'simple'}))


]
router = DefaultRouter()

router.register('goods/specs',spec.SpecView,base_name='spec')
urlpatterns += router.urls

router1 = DefaultRouter()
router1.register('skus',skus.SKUsView,base_name='skus')

urlpatterns += router1.urls