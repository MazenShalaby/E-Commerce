"""
URL configuration for e_commerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.conf import settings 
from django.conf.urls.static import static
from django.views.generic.base import TemplateView


urlpatterns = [
    # default apps routes
    path('admin/', admin.site.urls),
    
    # local apps routes
    path('accounts/', include('accounts.urls')),
    path('inventory/', include('inventory.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('coupons/', include('coupons.urls')),
    path("", TemplateView.as_view(template_name='home.html'), name='home'),
    
    # debugging & monitoring tools 
    path('silk/', include('silk.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)