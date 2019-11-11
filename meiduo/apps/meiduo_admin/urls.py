
from django.conf.urls import url
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token

from apps.meiduo_admin.views import admins
from apps.meiduo_admin.views import group
from .views import statistical,users
from . import views
from rest_framework.routers import DefaultRouter
from apps.meiduo_admin.views import spec,skus,options,images,spus,orders,permission,brand,channels

urlpatterns = [
    url(r'^authorizations/$', obtain_jwt_token),
    url(r'^statistical/total_count/$',statistical.UserTotalCountView.as_view()),
    url(r'^statistical/day_increment/$',statistical.UserDayCountView.as_view() ),
    url(r'^statistical/day_orders/$',statistical.UserOrderCountView.as_view() ),
    url(r'^statistical/month_increment/$',statistical.UserMouthCountView.as_view() ),
    url(r'^statistical/day_active/$',statistical.UserCountView.as_view() ),
    url(r'^statistical/goods_day_views/$',statistical.UserGoodsDayView.as_view() ),
    url(r'^users/$',users.UsersView.as_view() ),
    url(r'^goods/simple/$',spec.SpecView.as_view({'get':'simple'})),
    url(r'^goods/specs/simple/$',options.OptionView.as_view({'get':'simple'})),
    url(r'^skus/simple/$',images.ImageView.as_view({'get':'simple'})),
    url(r'^skus/categories/$',skus.SKUsView.as_view({'get':'simple'})),
    url(r'^goods/(?P<pk>\d+)/specs/$',skus.SKUsView.as_view({'get':'specs'})),
    url(r'^goods/brands/simple/$',spus.SPUView.as_view({'get':'simple'})),
    url(r'^goods/channel/categories/$',spus.SPUView.as_view({'get':'channel'})),
    url(r'^goods/channel/categories/(?P<pk>\d+)/$',spus.SPUView.as_view({'get':'channels'})),
    url(r'^goods/images/$',spus.SPUView.as_view({'post':'images'})),
    url(r'^orders/(?P<order_id>\d+)/status/$',orders.OrderView.as_view({'put':'status'})),
    url(r'^permission/content_types/$',permission.PermissionView.as_view({'get':'content_types'})),
    url(r'^permission/simple/$',group.GroupView.as_view({'get':'simple'})),
    url(r'^permission/groups/simple/$',admins.AdminView.as_view({'get':'groups'})),
    url(r'^goods/channel_types/$',channels.ChannelView.as_view({'get':'channel_types'})),
    url(r'^goods/categories/$',channels.ChannelView.as_view({'get':'categories'})),


]
router = DefaultRouter()

router.register('goods/specs',spec.SpecView,base_name='spec')
router.register('specs/options',options.OptionView,base_name='options')
router.register('skus/images',images.ImageView,base_name='images')
router.register('skus',skus.SKUsView,base_name='skus')

router.register('orders',orders.OrderView,base_name='orders')
router.register('permission/perms',permission.PermissionView,base_name='permission')
router.register('goods/brands',brand.BrandView,base_name='brands')
router.register('goods/channels',channels.ChannelView,base_name='channels')
router.register('goods',spus.SPUView,base_name='spus')
router.register('permission/groups',group.GroupView,base_name='group')
router.register('permission/admins',admins.AdminView,base_name='admins')

urlpatterns += router.urls





