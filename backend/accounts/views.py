from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer, CustomTokenObtainPairSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_users(request):
    if request.user.role not in ['admin', 'operator']:
        return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
    
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_user_role(request, user_id):
    if request.user.role != 'admin':
        return Response({"error": "Only admins can update roles"}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        user = User.objects.get(id=user_id)
        new_role = request.data.get('role')
        
        if new_role not in dict(User.ROLE_CHOICES):
            return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.role = new_role
        user.save()
        
        return Response(UserSerializer(user).data)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
