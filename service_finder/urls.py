from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'service_finder.views.home', name='home'),
    url(r'^finding/', include('finding.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
