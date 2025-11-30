from rest_framework import serializers
from .models import Resource, AutoScalingRule

class ResourceSerializer(serializers.ModelSerializer):

    def validate_cpu_cores(self, value):
        if value < 1:
            raise serializers.ValidationError("CPU cores must be at least 1.")
        return value

    def validate_memory_gb(self, value):
        if value < 1:
            raise serializers.ValidationError("Memory (GB) must be at least 1.")
        return value

    def validate_storage_gb(self, value):
        if value < 1:
            raise serializers.ValidationError("Storage (GB) must be at least 1.")
        return value

    class Meta:
        model = Resource
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']

class AutoScalingRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoScalingRule
        fields = '__all__'
