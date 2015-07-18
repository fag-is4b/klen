# This Python file uses the following encoding: utf-8

from django.conf.urls.defaults import *
from klen.main.views import main_show, parse, parse1, xls_write, row_edit, row_delete, logout_view, show_sind

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^klen/', include('klen.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    url(r'^$', main_show, name="main-show"),
    url(r'^parse/$', parse, name="parse"),
    url(r'^parse1/$', parse1, name="parse1"),
    url(r'^xls_write/$', xls_write, name="xls_write"),
    url(r'^row_edit/(\d+)/$', row_edit, name="row_edit"),
    url(r'^row_delete/(\d+)/$', row_delete, name="row_delete"),

    url(r'^logout/$', logout_view, name="logout_view"),

    url(r'^sindika/$', show_sind, name="show_sind"),

)

from django.shortcuts import render_to_response
from django.template import RequestContext

def handler404(request):
    print '-404-'
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    print '-500-'
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response