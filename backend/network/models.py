from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from resources.models import Resource

User = get_user_model()

class NetworkPolicy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='network_policies')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    ip_range = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.ip_range}"

class FirewallRule(models.Model):
    PROTOCOL_CHOICES = (
        ('tcp', 'TCP'),
        ('udp', 'UDP'),
        ('icmp', 'ICMP'),
    )
    
    ACTION_CHOICES = (
        ('allow', 'Allow'),
        ('deny', 'Deny'),
    )
    
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='firewall_rules')
    name = models.CharField(max_length=100)
    protocol = models.CharField(max_length=10, choices=PROTOCOL_CHOICES)
    port_range = models.CharField(max_length=20)
    source_ip = models.CharField(max_length=50, default='0.0.0.0/0')
    action = models.CharField(max_length=10, choices=ACTION_CHOICES, default='allow')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.protocol}:{self.port_range}"
