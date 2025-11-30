from rest_framework import serializers
from .models import BillingRecord, Budget

class BillingRecordSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    resource_name = serializers.CharField(source='resource.name', read_only=True)
    
    class Meta:
        model = BillingRecord
        fields = '__all__'

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'
        read_only_fields = ['user']
