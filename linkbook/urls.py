from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib import admin

import notifications.urls

from linkbook.core import views as linkbook_core_views
from linkbook.authentication import views as linkbook_auth_views
from linkbook.links import views as linkbook_link_views


urlpatterns = [
    url(r'^administrator/', admin.site.urls),
    url(r'^login', auth_views.login, {'template_name': 'authentication/login.html',
    	'redirect_authenticated_user': True}, name = 'login'),
    url(r'^logout', auth_views.logout, {'next_page': '/'}, name = 'logout'),
    url(r'^signup/$', linkbook_auth_views.signup, name = 'signup'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),

    url(r'^navbar/$', linkbook_core_views.navbar, name = 'navbar'),
    url(r'^inbox/notifications/', include(notifications.urls, namespace='notifications')),

    url(r'^link/(?P<id>\d+)/$', linkbook_link_views.link, name='link'),
    url(r'^link/new/$', linkbook_link_views.create_link, name = 'create_link'),
    url(r'^link/(?P<id>\d+)/edit/$', linkbook_link_views.edit_link, name='edit_link'),    
    url(r'^link/(?P<id>\d+)/vote/$', linkbook_link_views.vote_link, name = 'vote_link'),
    url(r'comment/load/', linkbook_link_views.ajax_load_comment, name = 'ajax_load_comment'),
    url(r'comment/create/', linkbook_link_views.ajax_create_comment, name = 'ajax_create_comment'),

    url(r'^tags/(?P<tag_name>[-\w]+)/$', linkbook_link_views.view_tag, name='view_tag'),

    url(r'^book/(?P<id>\d+)/$', linkbook_link_views.book, name='book'),
    url(r'^book/(?P<id>\d+)/edit/$', linkbook_link_views.edit_book, name='edit_book'),
    url(r'^book/new/$', linkbook_link_views.create_book, name = 'create_book'),
    url(r'^import/(?P<id>\d+)/$', linkbook_link_views.import_link, name='import_link'),

    url(r'^follow/$', linkbook_core_views.follow_profile, name = 'follow_profile'),    
    url(r'^followers/$', linkbook_core_views.get_follower_list, name = 'get_follower_list'),    
    url(r'^following/$', linkbook_core_views.get_following_list, name = 'get_following_list'),    
    url(r'^(?P<username>[-\w]+)/$', linkbook_core_views.username_slugs, name='username'),
    url(r'^(?P<username>[-\w]+)/edit/$', linkbook_core_views.edit_profile, name='edit_profile'),
    url(r'^$', linkbook_core_views.index, name = 'index'),
]
