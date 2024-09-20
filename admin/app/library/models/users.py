
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from utils.models import AuditableModel

# The user place holder model on the library db
class User(AuditableModel, AbstractBaseUser, PermissionsMixin):
    """ Custom user for application. """
    
    email = models.EmailField(max_length=125, unique=True, null=False, blank=False)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True)
    verified = models.BooleanField(default=False)
    

    USERNAME_FIELD = "email"
    
    def __str__(self):
        return f"{self.full_name} |{ self.email}".strip()
    
    @property
    def full_name(self):
        return f"{self.get_full_name()}"

    def get_full_name(self):
        return f"{self.firstname} {self.lastname}".strip()

