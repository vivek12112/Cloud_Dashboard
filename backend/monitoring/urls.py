from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MetricViewSet, AlertViewSet, generate_mock_metrics, get_dashboard_stats

router = DefaultRouter()
router.register(r'metrics', MetricViewSet, basename='metric')
router.register(r'alerts', AlertViewSet, basename='alert')

urlpatterns = [
    path('', include(router.urls)),
    path('generate-metrics/', generate_mock_metrics, name='generate_metrics'),
    path('dashboard-stats/', get_dashboard_stats, name='dashboard_stats'),
]
