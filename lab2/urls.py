from django.conf.urls import patterns, include, url

from lab2 import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^auth/$', views.auth, name='auth'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^auth/check/$', views.auth_check, name='auth_check'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register/post/$', views.register_post, name='register_post'),
    url(r'^account/$', views.account, name='account'),
    url(r'^users/me/$', views.userinfo, name="userinfo"),
    url(r'^auth/token/$', views.token, name='token'),

)