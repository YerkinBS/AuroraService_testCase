from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.conf import settings
import os


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)


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