from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from core.views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'core.views.index', name="index"),
    url(r'^data$', 'core.views.req_stats', name="data"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^requests/$',login_required(RequestListView.as_view())),
    url(r'^requests/([\d-]+)/$', login_required(RequestView.as_view())),
    url(r'^requests/add/$', login_required(RequestCreate.as_view())),
    url(r'^requests/([\d-]+)/edit$', login_required(RequestUpdate.as_view())),
    url(r'^requests/([\d-]+)/delete$', login_required(RequestDelete.as_view())),
    url(r'^responses/([\d-]+)/$', login_required(ResponseView.as_view())),
    url(r'^responses/([\d-]+)/edit$', login_required(ResponseView.as_view())),
    url(r'^responses/([\d-]+)/delete$', login_required(ResponseView.as_view())),
#/accounts/login/
    url(r'^accounts/login','django.contrib.auth.views.login'),
    url(r'^accounts/logout','django.contrib.auth.views.logout', {'next_page':'/'}),

)
