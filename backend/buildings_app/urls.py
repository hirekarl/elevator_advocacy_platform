from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BuildingViewSet, ReportViewSet

router = DefaultRouter()
router.register(r'buildings', BuildingViewSet, basename='building')
router.register(r'reports', ReportViewSet, basename='report')

urlpatterns = [
    path('', include(router.urls)),
]
