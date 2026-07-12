from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# Create your models here.


class AccountManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("User must have an email address!")
        if not password:
            raise ValueError("Password is required to provide!")
        
        user_obj = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_active'] = True
        extra_fields['is_staff'] = True
        extra_fields['is_admin'] = True
        extra_fields['is_superuser'] = True
        return self.create_user(email, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    
    class Gender(models.TextChoices):
        MALE = ("M", 'Male')
        FEMALE = ("F", 'Female')
    
    email = models.EmailField(max_length=50, unique=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    age = models.PositiveIntegerField(null=True)
    gender = models.CharField(max_length=6, choices=Gender.choices, null=True)
    profile_picture = models.ImageField(upload_to='profile_picture/images')
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = AccountManager()
    
    def __str__(self):
        return self.email 
