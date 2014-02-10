from django.conf.urls import patterns, url
from finding import views




urlpatterns = patterns('',
                       url(r'^$', views.home),
                   )
