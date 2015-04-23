from django.conf.urls import patterns, include, url

from lab2 import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^auth/$', views.auth, name='auth'),
    url(r'^auth/check/$', views.auth_check, name='auth_check'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register/post/$', views.register_post, name='register_post'),
    url(r'^account/$', views.account, name='account'),
    url(r'^userinfo/$', views.userinfo, name="userinfo"),
    url(r'^auth/token/$', views.token, name='token'),
    url(r'^country/$', views.country, name='country'),
    url(r'^city/$', views.city, name='city'),
    url(r'^monument/$', views.monument, name='monument'),
)