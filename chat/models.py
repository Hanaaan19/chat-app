from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone 

class CustomUser(AbstractUser):
    email=models.EmailField(unique=True)
    is_online=models.BooleanField(default=False)
    last_seen=models.DateTimeField(null=True,blank=True)


class Message(models.Model):
    sender=models.ForeignKey(CustomUser,related_name='sent_messages',on_delete=models.CASCADE)
    receiver=models.ForeignKey(CustomUser,related_name='received_messages',on_delete=models.CASCADE)
    content=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)
    is_read=models.BooleanField(default=False)

    class Meta:
        ordering=['timestamp']
