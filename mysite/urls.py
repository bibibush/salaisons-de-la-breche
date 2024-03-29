"""
URL configuration for mysite project.

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
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.static import serve
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from api.models import Order

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html"), name='index'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('user/', include('users.urls')),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),name="robot.txt"),
    path('sitemap.xml',TemplateView.as_view(template_name="sitemap.xml", content_type="application/xml"), name="sitemap"),
    re_path(r'.*', TemplateView.as_view(template_name='index.html'), name='react'),
    # re_path(r'^static/(?P<path>.*)$', serve, {'document_root' : settings.STATIC_ROOT}),
    # re_path(r'.*', TemplateView.as_view(template_name = 'index.html'), name= 'react-web')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
