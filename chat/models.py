from django.contrib.auth.models import User
from django.db import models

SEE = [
    ('unseen', 'unseen'),
    ('present', 'present'),
    ('seen', 'seen'),
]


class Message(models.Model):
    content = models.TextField()
    chat_pic = models.ImageField(upload_to='chat_pics/', null=True, blank=True)
    user1 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sender")
    user2 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="receiver")
    status = models.CharField(max_length=10, choices=SEE, default='unseen')
    created_on = models.DateTimeField(auto_now_add=True)
