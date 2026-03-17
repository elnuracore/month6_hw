from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users.managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)  
    first_name=models.CharField(max_length=30, blank=True, null=True)
    last_name=models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=20, unique=True, blank=True, null=True) 
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    birthdate=models.DateField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"    
    REQUIRED_FIELDS = ["phone_number", "birthdate"]
           

    def __str__(self):
        return self.email

class Confirm(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.user.email
