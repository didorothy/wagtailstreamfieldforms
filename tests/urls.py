from django.conf.urls import url, include
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
#from wagtailstreamfieldforms import urls as streamfieldforms_urls


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^cms/', include(wagtailadmin_urls)),
#    url(r'^forms/', include(streamfieldforms_urls)),
    url(r'', include(wagtail_urls)),
]