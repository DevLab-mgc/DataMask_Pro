from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('api-auth/', include('rest_framework.urls')),  # Adds login/logout views
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serves media files in development
