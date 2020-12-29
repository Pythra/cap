
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import Textarea, TextInput, EmailInput, NumberInput, FileInput
from .models import Profile, Announcement, Comment, Reply, Post
from django import forms


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'first_name', 'last_name', 'job', 'dp', 'balance'
        )

        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'first_name'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'last_name'}),
            'job': TextInput(attrs={'class': 'form-control'}),
        }


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# User update form allows users to update user name and email
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'username'}),
        }


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = (
            'body',
        )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', 'comment_pic')
        widgets = {
            'body': Textarea(attrs={
                'style': 'border-radius:7px; width:100%; height:60px; font-size:14px; padding:4px; border:1px solid grey;',
                'placeholder': 'Write a comment',
                'rows': '4'}),
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('body', 'comment_pic')
        widgets = {'body': Textarea(
            attrs={'class': 'form-control', 'rows': '3', 'placeholder': "Write a reply to this comment"})}


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'post_pic')
        widgets = {
            'title': Textarea(attrs={'class': 'form-control is_invalid', 'rows': '1', 'placeholder': 'Headline', 'style':'font-size:15px'}),
            'content': Textarea(attrs={'class': 'form-control', 'placeholder': 'Body', 'style':'font-size:15px'})}

