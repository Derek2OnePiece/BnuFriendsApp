from django.conf.urls.defaults import patterns

urlpatterns = patterns('BnuFriendsAppServer.src.views.email_views',
    (r'^send_email$', 'send_email_action'),
    (r'^get_email$', 'get_email_action'),
    (r'^get_email_count$', 'get_email_count_action'),
)
