from django.db import models
from django.contrib.auth.models import User


#chat
from django.db import models
from django.contrib.auth.models import User
from property.models import Property

class ChatMessage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='chats')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Chat on {self.property.title} - {self.sender.username} to {self.receiver.username}"
