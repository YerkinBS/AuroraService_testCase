from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.conf import settings
import os


class MainUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password=password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MainUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class Document(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='documents/', null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    def __repr__(self):
        return f'<Document: ({self.name}, {self.file}, {self.description})>'
    
    def __str__(self):
        return self.name

    def delete_file(self):
        if self.file:
            file_path = os.path.join(settings.MEDIA_ROOT, self.file.name)
            if os.path.exists(file_path):
                os.remove(file_path)

@receiver(pre_delete, sender=Document)
def delete_document_file(sender, instance, **kwargs):
    instance.delete_file()