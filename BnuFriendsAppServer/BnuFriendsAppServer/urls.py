from django.conf.urls import patterns, include, url
from BnuFriendsAppServer import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BnuFriendsAppServer.views.home', name='home'),
    # url(r'^BnuFriendsAppServer/', include('BnuFriendsAppServer.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    (r'^appserver/user/', include('BnuFriendsAppServer.src.urls.user_urls')),
    (r'^appserver/news/', include('BnuFriendsAppServer.src.urls.news_urls')),
    (r'^appserver/comment/', include('BnuFriendsAppServer.src.urls.comment_urls')),
    (r'^appserver/revision/', include('BnuFriendsAppServer.src.urls.revision_urls')),
    (r'^appserver/email/', include('BnuFriendsAppServer.src.urls.email_urls')),
    (r'^appserver/p/images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.IMAGES_PATH}),
    (r'^appserver/repos/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.REPOS_PATH}),

)
