
from rest_framework.decorators import api_view as shop_api
from rest_framework.response import Response
from .serializers import RegisterSerializer, ConfirmSerializer, LoginSerializer
from .models import Confirm
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers import CustomTokenObtainPairSerializer


class CUstomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterAPIView(APIView):
     @swagger_auto_schema(request_body=RegisterSerializer)
     def post (self, request):
      serializer = RegisterSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      result = serializer.save()
      return Response({
        "message": "User created",
        "code": result["code"]
    })
class ConfirmAPIView(APIView):
     @swagger_auto_schema(request_body=RegisterSerializer)
     def post(self, request):
      serializer = ConfirmSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      user = serializer.validated_data
      user.is_active = True
      user.save()
      Confirm.objects.get(user=user).delete()
      token, _ = Token.objects.get_or_create(user=user)
      return Response({"message": "User confirmed",
                       "token": token.key})
 
class LoginAPIView(APIView):
     @swagger_auto_schema(request_body=RegisterSerializer)
     def post(self, request):
      serializer = LoginSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      return Response({"message": "Login success"})
