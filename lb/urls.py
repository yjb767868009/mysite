from django.conf.urls import url

from . import views

app_name='lb'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^environment/(?P<pk>[0-9]+)/$', views.environment_detail, name='environment_detail'),
    url(r'^submission/$', views.submission, name='submission'),
    url(r'^accounts/profile/$', views.account_profile, name='account_profile'),
]

