from django.conf.urls import url

from . import views

app_name='lb'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^environment/(?P<pk>[0-9]+)/$', views.environment, name='environment'),
    url(r'^submission/(?P<pk>[0-9]+)/$', views.submission, name='submission'),
    url(r'^accounts/profile/$', views.account_profile, name='account_profile'),
    url(r'^accounts/detial/$', views.account_detail, name='account_detail'),
    url(r'^submit/$', views.submit, name='submit'),
]