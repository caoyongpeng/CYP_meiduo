from django.conf.urls import url
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token

from apps.meiduo_admin.views import images
from .views import statistical,users,specs,options
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    url(r'^authorizations/$', obtain_jwt_token),
    url(r'^statistical/total_count/$',statistical.UserTotalCountView.as_view()),
    url(r'^statistical/day_increment/$',statistical.UserDayCountView.as_view() ),
    url(r'^statistical/day_orders/$',statistical.UserOrderCountView.as_view() ),
    url(r'^statistical/month_increment/$',statistical.UserMouthCountView.as_view() ),
    url(r'^statistical/day_active/$',statistical.UserCountView.as_view() ),
    url(r'^statistical/goods_day_views/$',statistical.UserGoodsDayView.as_view() ),
    url(r'^users/$',users.UsersView.as_view()),
    url(r'^goods/simple/$',specs.SpecView.as_view({'get':'simple'})),
    url(r'^goods/specs/simple/$',options.OptionsView.as_view({'get':'simple'})),
    url(r'^skus/simple/$',images.ImageView.as_view({'get':'simple'})),


]
router = DefaultRouter()

router.register('goods/specs',specs.SpecView,base_name='spec')
router.register('specs/options',options.OptionsView,base_name='options')
router.register('skus/images',images.ImageView,base_name='images')
urlpatterns += router.urls