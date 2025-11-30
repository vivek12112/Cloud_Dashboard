from django.db import models

# Create your models here.
from django.db import models
from resources.models import Resource
from django.contrib.auth import get_user_model

User = get_user_model()

class Metric(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='metrics')
    cpu_usage = models.FloatField(default=0.0)
    memory_usage = models.FloatField(default=0.0)
    network_in = models.FloatField(default=0.0)
    network_out = models.FloatField(default=0.0)
    disk_usage = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Metrics for {self.resource.name} at {self.timestamp}"

class Alert(models.Model):
    SEVERITY_CHOICES = (
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alerts')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='alerts', null=True, blank=True)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='info')
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.severity.upper()} - {self.message[:50]}"
