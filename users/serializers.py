from rest_framework import serializers
from django.contrib.auth import authenticate
import random
from .models import Confirm, CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class OAuthCodeSerializer(serializers.Serializer):
    code = serializers.CharField()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["is_staff"] = user.is_staff
        token["birthdate"] = user.birthdate.isoformat() if user.birthdate else None

        return token

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    birthdate = serializers.CharField(required=False, allow_null=True)
    password = serializers.CharField()

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data["email"],
            phone_number=validated_data.get("phone_number") or None,
            birthdate=validated_data.get("birthdate"),
            is_active=False
        )
        user.set_password(validated_data["password"])
        user.save()
        code = str(random.randint(100000, 999999))
        Confirm.objects.create(user=user, code=code)
        return {"user": user, "code": code}


class ConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()
    def validate(self, data):
        try:
            user = CustomUser.objects.get(email=data["email"])
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User not found")
        try:
            confirm = Confirm.objects.get(user=user)
        except Confirm.DoesNotExist:
            raise serializers.ValidationError("Confirmation code not found")
        if confirm.code != data["code"]:
            raise serializers.ValidationError("Wrong code")
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_null=True)
    phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    password = serializers.CharField()
    def validate(self, data):
        password = data["password"]
        email = data.get("email")
        phone = data.get("phone_number")
        if not email and not phone:
            raise serializers.ValidationError("Send email or phone_number")
        if phone:
            try:
                u = CustomUser.objects.get(phone_number=phone)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError("Wrong username or password")
            if not u.is_superuser:
                raise serializers.ValidationError("Login by phone is only for superusers")
            user = authenticate(email=u.email, password=password)
        else:
            user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Wrong username or password")
        if not user.is_active:
            raise serializers.ValidationError("User not confirmed")
        return user