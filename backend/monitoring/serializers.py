from rest_framework import serializers
from .models import Metric, Alert

class MetricSerializer(serializers.ModelSerializer):
    resource_name = serializers.CharField(source='resource.name', read_only=True)
    
    class Meta:
        model = Metric
        fields = '__all__'

class AlertSerializer(serializers.ModelSerializer):
    resource_name = serializers.CharField(source='resource.name', read_only=True)
    
    class Meta:
        model = Alert
        fields = '__all__'
        read_only_fields = ['user', 'created_at']
