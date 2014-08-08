from django.conf.urls import patterns, include, url

from dgsproxy.views import ResourceView, StatsView


urlpatterns = [
    url(r'^stats', StatsView.as_view(), name='dgsproxy-stats'),
    url(r'^(?P<type>\w+)/(?P<uri>.*)$', ResourceView.as_view(), name='dgsproxy-root'),
]
