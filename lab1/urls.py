from django.conf.urls import patterns, include, url

from lab1 import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^code/', views.getcode, name='getcode'),
    url(r'^token/', views.gettoken, name='gettoken')
)