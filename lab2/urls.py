from django.conf.urls import patterns, include, url

from lab2 import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^authorize/$', views.authorize, name='authorize'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register/post/$', views.register_post, name='register_post'),
)