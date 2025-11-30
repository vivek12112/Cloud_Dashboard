from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from resources.models import Resource

User = get_user_model()

class BillingRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='billing_records')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='billing_records')
    usage_hours = models.DecimalField(max_digits=10, decimal_places=2)
    cost_per_hour = models.DecimalField(max_digits=8, decimal_places=4)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    billing_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-billing_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.resource.name} - ${self.total_cost}"

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    alert_threshold = models.IntegerField(default=80, help_text="Percentage at which to send alert")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Budget for {self.user.username} - ${self.limit}"
