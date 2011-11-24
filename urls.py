from django.conf.urls.defaults import *
from ideas import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template
from ideas.models import *


# this comment is to make sure github is working.
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'i2.views.home', name='home'),
    # url(r'^i2/', include('i2.foo.urls')),

    #(r'^$', index),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('ideas.views',
    (r'^$', 'index'),
    (r'^ajaxideadetail/', 'testthisajax'),
)

urlpatterns += staticfiles_urlpatterns()
