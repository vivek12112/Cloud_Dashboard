from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NetworkPolicyViewSet, FirewallRuleViewSet

router = DefaultRouter()
router.register(r'policies', NetworkPolicyViewSet, basename='network_policy')
router.register(r'firewall-rules', FirewallRuleViewSet, basename='firewall_rule')

urlpatterns = [
    path('', include(router.urls)),
]
