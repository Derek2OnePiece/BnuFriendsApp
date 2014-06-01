from django.conf.urls.defaults import patterns

urlpatterns = patterns('BnuFriendsAppServer.src.views.user_views',
    (r'^register$', 'register_action'),
    (r'^login$', 'login_action'),
    (r'^update_user_profile$', 'update_user_profile_action'),
    (r'^get_user_profile$', 'get_user_profile_action'),
    (r'^search_friends$', 'search_friends_action'),  
)
