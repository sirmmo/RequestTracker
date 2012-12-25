from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from core.views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'core.views.index', name="index"),
    url(r'^data$', 'core.views.req_stats', name="data"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^requests/$','core.views.req_list'),
    url(r'^requests/([\d-]+)/$', 'core.views.req_info'),
    url(r'^requests/add/$', 'core.views.req_edit'),
    url(r'^requests/([\d-]+)/edit$', 'core.views.req_edit'),
    url(r'^requests/([\d-]+)/delete$', 'core.views.req_delete'),
    url(r'^response/([\d-]+)/$', 'core.views.res_info'),
    url(r'^response/([\d-]+)/add$', 'core.views.res_edit'),
    url(r'^responses/([\d-]+)/edit$', 'core.views.res_edit'),
#/accounts/login/
    url(r'^accounts/login','django.contrib.auth.views.login'),
    url(r'^accounts/logout','django.contrib.auth.views.logout', {'next_page':'/'}),

)
