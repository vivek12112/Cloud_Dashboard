from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Resource(models.Model):
    RESOURCE_TYPE_CHOICES = (
        ('vm', 'Virtual Machine'),
        ('storage', 'Storage Bucket'),
        ('database', 'Database'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending Approval'),
        ('running', 'Running'),
        ('stopped', 'Stopped'),
        ('terminated', 'Terminated'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resources')
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPE_CHOICES)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Configuration stored as JSON-like fields
    cpu_cores = models.IntegerField(default=1)
    memory_gb = models.IntegerField(default=2)
    storage_gb = models.IntegerField(default=20)
    
    cost_per_hour = models.DecimalField(max_digits=8, decimal_places=4, default=0.05)
    region = models.CharField(max_length=50, default='us-east-1')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.get_resource_type_display()}) - {self.user.username}"

class AutoScalingRule(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='scaling_rules')
    metric_type = models.CharField(max_length=50, default='cpu_usage')
    threshold = models.FloatField()
    action = models.CharField(max_length=20, choices=[('scale_up', 'Scale Up'), ('scale_down', 'Scale Down')])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Scaling rule for {self.resource.name}"
