from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BillingRecordViewSet, BudgetViewSet, get_billing_summary, generate_mock_billing

router = DefaultRouter()
router.register(r'records', BillingRecordViewSet, basename='billing_record')
router.register(r'budgets', BudgetViewSet, basename='budget')

urlpatterns = [
    path('', include(router.urls)),
    path('summary/', get_billing_summary, name='billing_summary'),
    path('generate-mock/', generate_mock_billing, name='generate_mock_billing'),
]
