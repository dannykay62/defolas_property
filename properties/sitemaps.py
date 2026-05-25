from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Property


class PropertySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Property.objects.filter(status='available')

    def lastmod(self, obj):
        return obj.date_updated

    def location(self, obj):
        return obj.get_absolute_url()


class StaticViewSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return ['core:home', 'core:about', 'core:contact', 'properties:list']

    def location(self, item):
        return reverse(item)
