from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^user/$', views.user, name='user'),
    url(r'^environmnet/$', views.environment, name='environment'),
    url(r'^submission/$', views.submission, name='submission'),
]

