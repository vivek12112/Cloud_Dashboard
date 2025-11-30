from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Resource, AutoScalingRule
from .serializers import ResourceSerializer, AutoScalingRuleSerializer

class ResourceViewSet(viewsets.ModelViewSet):
    serializer_class = ResourceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role in ['admin', 'operator']:
            return Resource.objects.all()
        return Resource.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        resource = self.get_object()
        if resource.status == 'stopped':
            resource.status = 'running'
            resource.save()
            return Response({'status': 'Resource started'})
        return Response({'error': 'Resource is not in stopped state'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def stop(self, request, pk=None):
        resource = self.get_object()
        if resource.status == 'running':
            resource.status = 'stopped'
            resource.save()
            return Response({'status': 'Resource stopped'})
        return Response({'error': 'Resource is not running'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        if request.user.role not in ['admin', 'operator']:
            return Response({'error': 'Permission denied'}, 
                            status=status.HTTP_403_FORBIDDEN)
        
        resource = self.get_object()
        if resource.status == 'pending':
            resource.status = 'running'
            resource.save()
            return Response({'status': 'Resource approved and started'})
        return Response({'error': 'Resource is not pending'}, 
                        status=status.HTTP_400_BAD_REQUEST)
