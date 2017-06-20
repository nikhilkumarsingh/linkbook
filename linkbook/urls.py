from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib import admin

from linkbook.core import views as linkbook_core_views
from linkbook.authentication import views as linkbook_auth_views
from linkbook.links import views as linkbook_link_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login', auth_views.login, {'template_name': 'authentication/login.html',
    	'redirect_authenticated_user': True}, name = 'login'),
    url(r'^logout', auth_views.logout, {'next_page': '/'}, name = 'logout'),
    url(r'^signup/$', linkbook_auth_views.signup, name = 'signup'),

    url(r'^link/(?P<id>\d+)/$', linkbook_link_views.link, name='link'),
    url(r'^link/new/$', linkbook_link_views.create_link, name = 'create_link'),
    url(r'^link/(?P<id>\d+)/edit/$', linkbook_link_views.edit_link, name='edit_link'),    
    url(r'^link/(?P<id>\d+)/comment/$', linkbook_link_views.create_comment, name = 'create_comment'),
    url(r'^link/(?P<id>\d+)/vote/$', linkbook_link_views.vote_link, name = 'vote_link'),

    url(r'^tags/(?P<tag_name>[-\w]+)/$', linkbook_link_views.view_tag, name='view_tag'),

    url(r'^book/(?P<id>\d+)/$', linkbook_link_views.book, name='book'),
    url(r'^book/(?P<id>\d+)/edit/$', linkbook_link_views.edit_book, name='edit_book'),
    url(r'^book/new/$', linkbook_link_views.create_book, name = 'create_book'),
    
    url(r'^(?P<username>[\w.@+-]+/$)', linkbook_link_views.username_slugs, name='username'),
    
	url(r'^$', linkbook_core_views.index, name = 'index'),
]
