from django.forms import TextInput, forms
from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('content', 'chat_pic')
        widgets = {
            'content': TextInput(
                attrs={'class': 'form-control', 'id': "chat-message-input", 'type': "text"}),
        }
