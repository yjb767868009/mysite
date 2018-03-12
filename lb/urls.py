from django.conf.urls import url

from . import views

app_name='lb'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^environment/(?P<pk>[0-9]+)/Overview/$', views.environment, name='environment'),
    url(r'^environment/(?P<pk>[0-9]+)/Discussion/$',  views.environment_discussion, name='environment_discussion'),
    url(r'^environment/(?P<pk>[0-9]+)/Leaderboard/$',  views.environment_leaderboard, name='environment_leaderboard'),
    url(r'^environment/(?P<pk>[0-9]+)/Category/$',  views.environment_category, name='environment_category'),
    url(r'^submission/(?P<pk>[0-9]+)/Overview/$', views.submission, name='submission'),
    url(r'^submission/(?P<pk>[0-9]+)/BestRwards/$', views.submission_bestrwards, name='submission_bestrwards'),
    url(r'^submission/(?P<pk>[0-9]+)/Episodes/$', views.submission_episodes, name='submission_episodes'),
    url(r'^submission/(?P<pk>[0-9]+)/Discussion/$', views.submission_discussion, name='submission_discussion'),
    url(r'^accounts/profile/$', views.account_profile, name='account_profile'),
    url(r'^accounts/detail/(?P<username>[a-zA-Z0-9_\-\u4e00-\u9fa5]+)/$', views.account_detail, name='account_detail'),
    # url(r'^submit/$', views.submit, name='submit'),
    url(r'^environment_list/$', views.environment_list, name='environment_list'),
    # url(r'^search/$', views.search, name='search'),
]