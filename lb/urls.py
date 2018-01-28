from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^user/$', views.detail, name='user'),
    url(r'^environmnet/$', views.detail, name='environment'),
    url(r'^submission/$', views.detail, name='submission'),
]

