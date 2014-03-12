from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings


admin.autodiscover()


# Signal handlers
from wagtail.wagtailsearch import register_signal_handlers
register_signal_handlers()


urlpatterns = patterns('',
    url(r'^django-admin/', include(admin.site.urls)),

    url(r'^admin/images/', include('wagtail.wagtailimages.urls')),
    url(r'^admin/embeds/', include('wagtail.wagtailembeds.urls')),
    url(r'^admin/documents/', include('wagtail.wagtaildocs.admin_urls')),
    url(r'^admin/snippets/', include('wagtail.wagtailsnippets.urls')),
    url(r'^admin/search/', include('wagtail.wagtailsearch.urls.admin')),
    url(r'^admin/users/', include('wagtail.wagtailusers.urls')),
    url(r'^admin/redirects/', include('wagtail.wagtailredirects.urls')),
    url(r'^admin/', include('wagtail.wagtailadmin.urls')),
    url(r'^search/', include('wagtail.wagtailsearch.urls.frontend')),
    url(r'^documents/', include('wagtail.wagtaildocs.urls')),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's serving mechanism
    url(r'', include('wagtail.wagtailcore.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
