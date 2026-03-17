
from rest_framework.decorators import api_view as shop_api
from rest_framework.response import Response
from .serializers import RegisterSerializer, ConfirmSerializer, LoginSerializer
from .models import Confirm
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers import CustomTokenObtainPairSerializer
from django.core.cache import cache
# from users.tasks import send_otp
from users.tasks import send_welcome_email, long_running_task



class CUstomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RegisterAPIView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        user = result["user"]
        code = result["code"]
        send_welcome_email.delay(user.email)
        long_running_task.delay(20)
        return Response({
            "message": "User created",
            "code": code
        })
class ConfirmAPIView(APIView):
    @swagger_auto_schema(request_body=ConfirmSerializer)
    def post(self, request):
        serializer = ConfirmSerializer(data=request.data) 
        serializer.is_valid(raise_exception=True) 
        user = serializer.validated_data
        code = request.data["code"]
        redis_code = cache.get(f"confirm_code_{user.id}")
        print("REDIS CODE:", cache.get(f"confirm_code_{user.id}"))
        if not redis_code:
            return Response({"error": "Code expired or not found"}, status=400)
        if redis_code != code:
            return Response({"error": "Invalid code"}, status=400)
        user.is_active = True
        user.save()
        cache.delete(f"confirm_code_{user.id}")
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "message": "User confirmed",
            "token": token.key
        })
 
class LoginAPIView(APIView):
     @swagger_auto_schema(request_body=RegisterSerializer)
     def post(self, request):
      serializer = LoginSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      return Response({"message": "Login success"})