from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
# import random
# Create your models here.


class UserManager(BaseUserManager):
    """
    Custom User Model Manager where email is unique
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and Save a User with the given email and password. and extra data
        """
        if not email:
            raise ValueError(_("the Email most be set"))
        email = self.normalize_email(email)
        # self.model == به مدلی اشاره میکند که این منیجر برای آن ساخته شده است
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and Save a Superuser with the given email and password. and extra data
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser most have is_staff=True."))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser most have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model for our app
    """

    email = models.EmailField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    # is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return self.email

# first_name = models.CharField(max_length=250, default=f"user {random.randint(1, 9999)}")
class Profile(models.Model):
    """
    Profile Models for user instance:
    (create autho when create user)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    image = models.ImageField(upload_to="profile", blank=True, null=True)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    """
    Create Profile by receiver in signals
    with user instance: (auto when created a user)
    
    1.sender: our sender --> here is User class
    2.instance: our user instance of User model
    3.created: if instance created is True, but updated is False
    4.**kwargs: another parameters.... 
    """
    if created:
        Profile.objects.create(user=instance)
