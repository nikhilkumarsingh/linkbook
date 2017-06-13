from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib import admin

from linkbook.authentication import views as linkbook_auth_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login', auth_views.login, {'template_name': 'authentication/login.html'}, name = 'login'),
    url(r'^logout', auth_views.logout, {'next_page': '/'}, name = 'logout'),
    url(r'^signup/$', linkbook_auth_views.signup, name = 'signup'),
]
