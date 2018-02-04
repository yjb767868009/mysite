from django.conf.urls import url

from . import views

app_name='lb'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^environment/(?P<pk>[0-9]+)/$', views.environment, name='environment'),
    url(r'^submission/(?P<pk>[0-9]+)/$', views.submission, name='submission'),
    url(r'^accounts/profile/$', views.account_profile, name='account_profile'),
    url(r'^accounts/detail/(?P<username>[a-zA-Z0-9_\-\u4e00-\u9fa5]+)/$', views.account_detail, name='account_detail'),
    # url(r'^submit/$', views.submit, name='submit'),
    url(r'^environment_list/$', views.environment_list, name='environment_list'),
    # url(r'^search/$', views.search, name='search'),
]