from rest_framework import serializers
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True, allow_null=True)
    
    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']
