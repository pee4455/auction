from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Admin
from .serializers import AdminSerializer, LoginSerializer
import logging

logger = logging.getLogger(__name__)

# Create your views here.

@api_view(['POST'])
def admin_login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        try:
            admin = Admin.objects.get(username=username)
            logger.info(f"Found admin user: {username}")
            
            if admin.check_password(password):
                logger.info("Password check successful")
                return Response({
                    'status': 'success',
                    'message': 'Login successful',
                    'user': AdminSerializer(admin).data,
                    'token': 'your-jwt-token-here'  # ในการใช้งานจริงควรสร้าง JWT token
                })
            else:
                logger.warning(f"Invalid password for user: {username}")
                return Response({
                    'status': 'error',
                    'message': 'รหัสผ่านไม่ถูกต้อง'
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Admin.DoesNotExist:
            logger.warning(f"User not found: {username}")
            return Response({
                'status': 'error',
                'message': 'ไม่พบบัญชีผู้ใช้นี้'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Database error: {str(e)}")
            return Response({
                'status': 'error',
                'message': 'เกิดข้อผิดพลาดในการเชื่อมต่อฐานข้อมูล'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    logger.error(f"Invalid form data: {serializer.errors}")
    return Response({
        'status': 'error',
        'message': 'ข้อมูลไม่ถูกต้อง',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
