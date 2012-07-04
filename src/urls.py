from django.conf.urls.defaults import patterns, include, url

import saxes.sax_settings as sax_settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'saxes.views.home', name='home'),
    url(r'^posts/(()|(?P<post_pk>\d+))$', 'saxes.views.home', name='home'),
    url(r'^book/$', 'saxes.views.book', name='book'),
    url(r'^book/($|(?P<page>\w{0,50})$)', 'saxes.views.book', name='book'),
    url(r'^members/(()|(?P<year>\d+))$', 'saxes.views.members', name='members'),
    
    url(r'^gallery/$', 'saxes.views.gallery', name='gallery'),
    url(r'^friends/(()|(?P<friend>\w{0,50}))$', 'saxes.views.friends', name='friends'),
    
    url(r'^music/$', 'saxes.views.music', name='music'),
    url(r'^members_page/$', 'saxes.views.music', name='music'),
    
    #FORMS
    url(r'^login/$', 'saxes.views.login', name='login'),
    url(r'^add_quote/$', 'saxes.views.add_object', name='add_object', kwargs=sax_settings.ADD_QUOTE_KWARGS),
    url(r'^add_post/$', 'saxes.views.add_object', name='add_object', kwargs=sax_settings.ADD_POST_KWARGS),
    #Book URLS
    
    #TinyMCE
    (r'^tinymce/', include('tinymce.urls')),
    
    
    # url(r'^husky_saxes/', include('husky_saxes.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^photologue/', include('photologue.urls')),
)
