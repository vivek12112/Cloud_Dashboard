from rest_framework import serializers
from .models import NetworkPolicy, FirewallRule

class NetworkPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkPolicy
        fields = '__all__'
        read_only_fields = ['user']

class FirewallRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirewallRule
        fields = '__all__'
