from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    name = models.CharField(max_length=255)
    is_group = models.BooleanField(default=False)
    participants = models.ManyToManyField(User)

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

