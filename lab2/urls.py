from django.conf.urls import patterns, include, url

from lab2 import views

urlpatterns = patterns('',
    url(r'^$', views.auth, name='auth'),
    url(r'^auth/$', views.auth, name='auth'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register/post/$', views.register_post, name='register_post'),
    url(r'^account/$', views.account, name='account'),
    url(r'^users/me/$', views.userinfo, name="userinfo"),
    url(r'^auth/token/$', views.token, name='token'),
    url(r'^manufacturers/$', views.manufacturers, name='manufacturers'),
    url(r'^manufacturers/(?P<manufacturer_id>[0-9]+)/$', views.man_detail, name='man_detail'),
    url(r'^devices/$', views.devices, name='devices'),
    url(r'^devices/(?P<device_id>[0-9]+)/$', views.dev_detail, name='dev_detail'),
)