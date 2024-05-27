from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib import sitemaps
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from shop.sitemaps import ProductSitemap, StaticViewSitemap


sitemaps = {
    'products': ProductSitemap,
    'static': StaticViewSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('', include('erp.urls')),
    path('accounts/', include('allauth.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
