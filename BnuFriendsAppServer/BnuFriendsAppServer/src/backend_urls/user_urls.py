from django.conf.urls.defaults import patterns

urlpatterns = patterns('BnuFriendsAppServer.src.backend_views.user_views',
    (r'^login$', 'login_action'),

)
