from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import NetworkPolicy, FirewallRule
from .serializers import NetworkPolicySerializer, FirewallRuleSerializer

class NetworkPolicyViewSet(viewsets.ModelViewSet):
    serializer_class = NetworkPolicySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'engineer', 'operator']:
            return NetworkPolicy.objects.all()
        return NetworkPolicy.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FirewallRuleViewSet(viewsets.ModelViewSet):
    serializer_class = FirewallRuleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'engineer', 'operator']:
            return FirewallRule.objects.all()
        return FirewallRule.objects.filter(resource__user=user)
