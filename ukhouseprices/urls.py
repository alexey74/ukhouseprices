"""ukhouseprices URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
from pricepaid.views import (PricePaidEntryViewSet, PricePaidStatsViewSet,
                             TownViewSet, DistrictViewSet, CountyViewSet)

router = routers.DefaultRouter()
router.register(r'pricepaidentry', PricePaidEntryViewSet)
router.register(r'pricepaidstats', PricePaidStatsViewSet, base_name='pricepaidstats')
router.register(r'town', TownViewSet)
router.register(r'district', DistrictViewSet)
router.register(r'county', CountyViewSet)


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'pricepaid.views.index'),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'^pricepaidstats/$', PricePaidStatsView.as_view()),
]
