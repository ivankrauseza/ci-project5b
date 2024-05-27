from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return ['home', 'about', 'contact', 'privacy', 'cookie', 'support']

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Product.objects.filter(blocked=False)

    def lastmod(self, obj):
        return obj.updated

    def location(self, obj):
        return f'/product/{obj.sku}/'