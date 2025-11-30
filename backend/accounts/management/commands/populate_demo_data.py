from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from resources.models import Resource, AutoScalingRule
from monitoring.models import Metric, Alert
from billing.models import BillingRecord, Budget
from support.models import Ticket
from network.models import NetworkPolicy, FirewallRule
from datetime import datetime, timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate database with demo data for client presentation'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating demo data...')
        
        # Create demo users
        users = self.create_users()
        
        # Create resources
        resources = self.create_resources(users)
        
        # Create metrics
        self.create_metrics(resources)
        
        # Create alerts
        self.create_alerts(users, resources)
        
        # Create billing records
        self.create_billing_records(users, resources)
        
        # Create support tickets
        self.create_tickets(users)
        
        # Create network policies
        self.create_network_policies(users, resources)
        
        self.stdout.write(self.style.SUCCESS('✅ Demo data created successfully!'))
        self.stdout.write(self.style.SUCCESS('\nDemo Login Credentials:'))
        self.stdout.write('Admin: username=admin, password=admin123')
        self.stdout.write('User: username=john, password=pass123')
        self.stdout.write('Operator: username=operator, password=pass123')
        self.stdout.write('Analyst: username=analyst, password=pass123')

    def create_users(self):
        users = {}
        
        # Admin user
        if not User.objects.filter(username='admin').exists():
            users['admin'] = User.objects.create_user(
                username='admin',
                email='admin@cloudplatform.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
                role='admin',
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write('Created admin user')
        
        # Regular user
        if not User.objects.filter(username='john').exists():
            users['john'] = User.objects.create_user(
                username='john',
                email='john@example.com',
                password='pass123',
                first_name='John',
                last_name='Doe',
                role='user',
                organization='Tech Corp'
            )
            self.stdout.write('Created regular user: john')
        
        # Operator
        if not User.objects.filter(username='operator').exists():
            users['operator'] = User.objects.create_user(
                username='operator',
                email='operator@cloudplatform.com',
                password='pass123',
                first_name='Cloud',
                last_name='Operator',
                role='operator'
            )
            self.stdout.write('Created operator user')
        
        # Analyst
        if not User.objects.filter(username='analyst').exists():
            users['analyst'] = User.objects.create_user(
                username='analyst',
                email='analyst@cloudplatform.com',
                password='pass123',
                first_name='Finance',
                last_name='Analyst',
                role='analyst'
            )
            self.stdout.write('Created analyst user')
        
        return users

    def create_resources(self, users):
        resources = []
        user = users.get('john') or User.objects.filter(role='user').first()
        
        resource_configs = [
            {'name': 'Web Server 01', 'type': 'vm', 'cpu': 4, 'mem': 8, 'storage': 100, 'status': 'running'},
            {'name': 'Database Server', 'type': 'vm', 'cpu': 8, 'mem': 16, 'storage': 500, 'status': 'running'},
            {'name': 'Storage Bucket A', 'type': 'storage', 'cpu': 0, 'mem': 0, 'storage': 1000, 'status': 'running'},
            {'name': 'API Server', 'type': 'vm', 'cpu': 2, 'mem': 4, 'storage': 50, 'status': 'stopped'},
            {'name': 'Dev Environment', 'type': 'vm', 'cpu': 2, 'mem': 4, 'storage': 80, 'status': 'pending'},
        ]
        
        for config in resource_configs:
            resource = Resource.objects.create(
                user=user,
                name=config['name'],
                resource_type=config['type'],
                cpu_cores=config['cpu'],
                memory_gb=config['mem'],
                storage_gb=config['storage'],
                status=config['status'],
                cost_per_hour=round(0.05 + (config['cpu'] * 0.02) + (config['mem'] * 0.01), 4),
                region=random.choice(['us-east-1', 'us-west-2', 'eu-west-1', 'ap-south-1'])
            )
            resources.append(resource)
            
            # Add auto-scaling rule for VMs
            if config['type'] == 'vm' and config['status'] == 'running':
                AutoScalingRule.objects.create(
                    resource=resource,
                    metric_type='cpu_usage',
                    threshold=80.0,
                    action='scale_up',
                    is_active=True
                )
        
        self.stdout.write(f'Created {len(resources)} resources')
        return resources

    def create_metrics(self, resources):
        count = 0
        for resource in resources:
            if resource.status == 'running':
                # Create metrics for last 24 hours
                for i in range(24):
                    Metric.objects.create(
                        resource=resource,
                        cpu_usage=random.uniform(20, 85),
                        memory_usage=random.uniform(30, 75),
                        network_in=random.uniform(100, 5000),
                        network_out=random.uniform(100, 5000),
                        disk_usage=random.uniform(40, 70)
                    )
                    count += 1
        
        self.stdout.write(f'Created {count} metric records')

    def create_alerts(self, users, resources):
        user = users.get('john') or User.objects.filter(role='user').first()
        
        alerts = [
            {'severity': 'warning', 'msg': 'CPU usage above 80% on Web Server 01', 'resolved': False},
            {'severity': 'info', 'msg': 'Scheduled maintenance completed', 'resolved': True},
            {'severity': 'critical', 'msg': 'Database Server memory usage critical', 'resolved': False},
            {'severity': 'warning', 'msg': 'Network latency increased', 'resolved': True},
        ]
        
        for alert_data in alerts:
            Alert.objects.create(
                user=user,
                resource=resources[0] if resources else None,
                severity=alert_data['severity'],
                message=alert_data['msg'],
                is_resolved=alert_data['resolved']
            )
        
        self.stdout.write(f'Created {len(alerts)} alerts')

    def create_billing_records(self, users, resources):
        user = users.get('john') or User.objects.filter(role='user').first()
        count = 0
        
        for resource in resources:
            if resource.status in ['running', 'stopped']:
                # Create billing for last 30 days
                for i in range(30):
                    date = datetime.now().date() - timedelta(days=i)
                    hours = random.uniform(18, 24) if resource.status == 'running' else random.uniform(0, 8)
                    
                    BillingRecord.objects.create(
                        user=user,
                        resource=resource,
                        usage_hours=round(hours, 2),
                        cost_per_hour=resource.cost_per_hour,
                        total_cost=round(hours * float(resource.cost_per_hour), 2),
                        billing_date=date
                    )
                    count += 1
        
        # Create budget
        Budget.objects.get_or_create(
            user=user,
            defaults={
                'limit': 1000.00,
                'alert_threshold': 80,
                'is_active': True
            }
        )
        
        self.stdout.write(f'Created {count} billing records and budget')

    def create_tickets(self, users):
        user = users.get('john') or User.objects.filter(role='user').first()
        
        tickets = [
            {'title': 'Cannot access VM dashboard', 'desc': 'Getting 404 error when accessing dashboard', 'priority': 'high', 'status': 'open'},
            {'title': 'Request quota increase', 'desc': 'Need to increase storage quota for project', 'priority': 'medium', 'status': 'in_progress'},
            {'title': 'Billing inquiry', 'desc': 'Question about last month charges', 'priority': 'low', 'status': 'resolved'},
        ]
        
        for ticket_data in tickets:
            Ticket.objects.create(
                user=user,
                title=ticket_data['title'],
                description=ticket_data['desc'],
                priority=ticket_data['priority'],
                status=ticket_data['status']
            )
        
        self.stdout.write(f'Created {len(tickets)} support tickets')

    def create_network_policies(self, users, resources):
        user = users.get('john') or User.objects.filter(role='user').first()
        
        NetworkPolicy.objects.get_or_create(
            user=user,
            name='Default VPC',
            defaults={
                'description': 'Default network policy for VPC',
                'ip_range': '10.0.0.0/16',
                'is_active': True
            }
        )
        
        # Add firewall rules
        for resource in resources[:2]:
            if resource.resource_type == 'vm':
                FirewallRule.objects.get_or_create(
                    resource=resource,
                    name=f'Allow HTTP for {resource.name}',
                    defaults={
                        'protocol': 'tcp',
                        'port_range': '80',
                        'source_ip': '0.0.0.0/0',
                        'action': 'allow',
                        'is_active': True
                    }
                )
                
                FirewallRule.objects.get_or_create(
                    resource=resource,
                    name=f'Allow HTTPS for {resource.name}',
                    defaults={
                        'protocol': 'tcp',
                        'port_range': '443',
                        'source_ip': '0.0.0.0/0',
                        'action': 'allow',
                        'is_active': True
                    }
                )
        
        self.stdout.write('Created network policies and firewall rules')
