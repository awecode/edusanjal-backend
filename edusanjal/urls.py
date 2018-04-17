from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import include, url

from .api_urls import urlpatterns as api_urlpatterns

admin.site.site_header = 'Control Panel'

urlpatterns = [
                  url(r'^jet/', include('jet.urls', 'jet')),
                  path(settings.ADMIN_URL, admin.site.urls),
              ] + api_urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar

    urlpatterns = [
                      url(r'^__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
