from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, CustomTokenObtainPairView, get_current_user, list_users, update_user_role

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', get_current_user, name='current_user'),
    path('users/', list_users, name='list_users'),
    path('users/<int:user_id>/role/', update_user_role, name='update_user_role'),
]
