from django.conf.urls.defaults import patterns

urlpatterns = patterns('BnuFriendsAppServer.src.views.news_views',
    (r'^add_news$', 'add_news_action'),
    (r'list_news$', 'list_news_action'),
    (r'get_news_count$', 'get_news_count_action'),
    (r'get_news_detail$', 'get_news_detail_action'),
)
