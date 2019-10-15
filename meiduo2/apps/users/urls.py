from django.conf.urls import url



# def text(request):
#     logger = logging.getLogger('django')
#     logger.debug('测试logging模块debug')
#     return HttpResponse('text')
from . import views

urlpatterns = [
    url(r'^register/$',views.RegisterView.as_view())

]