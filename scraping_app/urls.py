"""
URL configuration for scraping_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from etl.views import ScrapingMetricsView, VikingsShowViewSet, NorsemenShowViewSet, NFLVikingsShowViewSet

router = DefaultRouter()
router.register(r"vikings", VikingsShowViewSet, basename="vikings_show")
router.register(r"norsemen", NorsemenShowViewSet, basename="norsemen_show")
router.register(r"vikings_nfl", NFLVikingsShowViewSet, basename="vikings_nfl")

# Define the URL patterns
urlpatterns = [
    path("metrics/", ScrapingMetricsView.as_view(), name="scraping-metrics"),
    path("admin/", admin.site.urls), path("api/", include(router.urls))]
