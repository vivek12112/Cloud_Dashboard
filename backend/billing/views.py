from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import BillingRecord, Budget
from .serializers import BillingRecordSerializer, BudgetSerializer
from resources.models import Resource
from datetime import datetime, timedelta
from decimal import Decimal

class BillingRecordViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BillingRecordSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role in ['admin', 'analyst']:
            return BillingRecord.objects.all()
        return BillingRecord.objects.filter(user=self.request.user)

class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role in ['admin', 'analyst']:
            return Budget.objects.all()
        return Budget.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_billing_summary(request):
    """Get billing summary for user"""
    user = request.user
    
    if user.role in ['admin', 'analyst']:
        total_cost = sum([br.total_cost for br in BillingRecord.objects.all()])
        monthly_cost = sum([br.total_cost for br in BillingRecord.objects.filter(
            billing_date__month=datetime.now().month
        )])
    else:
        total_cost = sum([br.total_cost for br in BillingRecord.objects.filter(user=user)])
        monthly_cost = sum([br.total_cost for br in BillingRecord.objects.filter(
            user=user,
            billing_date__month=datetime.now().month
        )])
    
    active_resources_cost = sum([
        float(r.cost_per_hour) for r in Resource.objects.filter(
            user=user, status='running'
        )
    ]) if user.role not in ['admin', 'analyst'] else 0
    
    return Response({
        'total_cost': float(total_cost),
        'monthly_cost': float(monthly_cost),
        'active_resources_hourly_cost': active_resources_cost,
        'estimated_monthly': active_resources_cost * 24 * 30,
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_mock_billing(request):
    """Generate mock billing records for demo"""
    resource_id = request.data.get('resource_id')
    
    try:
        resource = Resource.objects.get(id=resource_id)
        
        billing_record = BillingRecord.objects.create(
            user=resource.user,
            resource=resource,
            usage_hours=Decimal('24.00'),
            cost_per_hour=resource.cost_per_hour,
            total_cost=Decimal('24.00') * resource.cost_per_hour,
            billing_date=datetime.now().date()
        )
        
        return Response(BillingRecordSerializer(billing_record).data, status=status.HTTP_201_CREATED)
    except Resource.DoesNotExist:
        return Response({'error': 'Resource not found'}, status=status.HTTP_404_NOT_FOUND)
