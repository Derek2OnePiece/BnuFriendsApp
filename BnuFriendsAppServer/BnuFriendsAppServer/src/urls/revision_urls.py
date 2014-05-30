from django.conf.urls.defaults import patterns

urlpatterns = patterns('BnuFriendsAppServer.src.views.revision_views',
    (r'^get_revision$', 'get_revision_action'),
)
