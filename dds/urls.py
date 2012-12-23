from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from core.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dds.views.home', name='home'),
    # url(r'^dds/', include('dds.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^data$', 'core.views.req_stats'),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^requests/',login_required(RequestView.as_view()) ),

)
