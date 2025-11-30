from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Metric, Alert
from .serializers import MetricSerializer, AlertSerializer
from resources.models import Resource
from django.contrib.auth import get_user_model
import random
from datetime import datetime, timedelta

User = get_user_model()

class MetricViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MetricSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role in ['admin', 'operator']:
            return Metric.objects.all()
        return Metric.objects.filter(resource__user=self.request.user)

class AlertViewSet(viewsets.ModelViewSet):
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role in ['admin', 'operator', 'support']:
            return Alert.objects.all()
        return Alert.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_mock_metrics(request):
    """Generate mock metrics for demo purposes"""
    resource_id = request.data.get('resource_id')
    
    try:
        resource = Resource.objects.get(id=resource_id, user=request.user)
        
        # Generate random metrics
        metric = Metric.objects.create(
            resource=resource,
            cpu_usage=random.uniform(10, 90),
            memory_usage=random.uniform(20, 80),
            network_in=random.uniform(100, 10000),
            network_out=random.uniform(100, 10000),
            disk_usage=random.uniform(30, 70)
        )
        
        return Response(MetricSerializer(metric).data, status=status.HTTP_201_CREATED)
    except Resource.DoesNotExist:
        return Response({'error': 'Resource not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dashboard_stats(request):
    """Get overview statistics for dashboard"""
    user = request.user
    
    if user.role in ['admin', 'operator']:
        total_resources = Resource.objects.count()
        active_resources = Resource.objects.filter(status='running').count()
        total_users = User.objects.count()
    else:
        total_resources = Resource.objects.filter(user=user).count()
        active_resources = Resource.objects.filter(user=user, status='running').count()
        total_users = 1
    
    pending_resources = Resource.objects.filter(status='pending').count() if user.role in ['admin', 'operator'] else 0
    unresolved_alerts = Alert.objects.filter(is_resolved=False).count()
    
    return Response({
        'total_resources': total_resources,
        'active_resources': active_resources,
        'pending_resources': pending_resources,
        'total_users': total_users,
        'unresolved_alerts': unresolved_alerts,
    })
