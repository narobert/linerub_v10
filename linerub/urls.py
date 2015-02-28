from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'blog.views.home', name='home'),
    # url(r'^linerub/', include('linerub.foo.urls')),
    url(r'^logout/', 'blog.views.logout'),
    url(r'^login/', 'blog.views.login', name='login'),
    url(r'^register/', 'blog.views.register', name='register'),
    url(r'^faq/', 'blog.views.faq', name='faq'),
    url(r'^contact/', 'blog.views.contact', name='contact'),
    url(r'^create/', 'blog.views.create', name='create'),
    url(r'^dashboard/', 'blog.views.dashboard', name='dashboard'),
    url(r'^next/', 'blog.views.next', name='next'),
    url(r'^nextw/(?P<id>[\w\-]+)/$', 'blog.views.nextw', name='nextw'),
    url(r'^view/', 'blog.views.view', name='view'),
    url(r'^exchange/', 'blog.views.exchange', name='exchange'),
    url(r'^submit/', 'blog.views.submit', name='submit'),
    url(r'^tag/(?P<id>[\w\-]+)/(?P<word>[\w\-]+)/$', 'blog.views.tag', name='tag'),
    url(r'^highlight/', 'blog.views.highlight', name='highlight'),
    url(r'^highlightw/(?P<id>[\w\-]+)/$', 'blog.views.highlightw', name='highlightw'),
    url(r'^profile/(?P<username>[\w\-]+)/$', 'blog.views.profile', name='profile'),
    url(r'^follow/(?P<username>[\w\-]+)/$', 'blog.views.follow', name='follow'),
    url(r'^unfollow/(?P<username>[\w\-]+)/$', 'blog.views.unfollow', name='unfollow'),
    url(r'^like/(?P<id>[\w\-]+)/$', 'blog.views.like', name='like'),
    url(r'^unlike/(?P<id>[\w\-]+)/$', 'blog.views.unlike', name='unlike'),
    url(r'^delete/(?P<id>[\w\-]+)/$', 'blog.views.delete', name='delete'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
  urlpatterns += patterns('',
    (r'^css/(.*)$', 'django.views.static.serve',
      {'document_root': settings.STATIC_ROOT + "/css", 'show_indexes': True}),
    (r'^images/(.*)$', 'django.views.static.serve',
      {'document_root': settings.STATIC_ROOT + "/images", 'show_indexes': True}),
    (r'^js/(.*)$', 'django.views.static.serve',
      {'document_root': settings.STATIC_ROOT + "/js", 'show_indexes': True}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
      {'document_root': settings.STATIC_ROOT + "/media", 'show_indexes': True}),
  )
