from django.conf.urls import url

from . import views
urlpatterns = [
    url(r'^register/$',views.RegisterView.as_view()),
    url(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/$',views.RegisterCountView.as_view())
]