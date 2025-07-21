from django import forms
from .models import Post, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())  # Rich text editor

    class Meta:
        model = Post
        fields = ['title', 'content', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control text-dark',
                'placeholder': '📝 Enter magical title',
                'style': 'color: black;'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select text-dark',
                'style': 'color: black;'
            }),
        }

    class Media:
        js = [
            'ckeditor/ckeditor-init.js',
            'ckeditor/ckeditor/ckeditor.js'
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'body']
        widgets = {
            'author': forms.TextInput(attrs={
                'class': 'form-control text-dark',
                'placeholder': '👤 Your Name',
                'style': 'color: black;'
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control text-dark',
                'placeholder': '💬 Add a thoughtful comment...',
                'style': 'color: black;',
                'rows': 3
            }),
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control text-dark',
        'placeholder': '📧 Email address',
        'style': 'color: black;'
    }))

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control text-dark',
        'placeholder': '👤 Username',
        'style': 'color: black;'
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control text-dark',
        'placeholder': '🔒 Password',
        'style': 'color: black;'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control text-dark',
        'placeholder': '🔐 Confirm Password',
        'style': 'color: black;'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
