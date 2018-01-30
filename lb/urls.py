from django.conf.urls import url

from . import views

app_name='lb'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^environment/$', views.environment, name='environment'),
    url(r'^submission/$', views.submission, name='submission'),
    url(r'^accounts/profile/$', views.account_profile, name='account_profile'),
]

