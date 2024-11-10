from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'files', views.FileUploadViewSet)
router.register(r'logs', views.ProcessingLogViewSet, basename='processinglog')
router.register(r'detections', views.PIIDetectionViewSet, basename='piidetection')

urlpatterns = [
    path('', include(router.urls)),
]
