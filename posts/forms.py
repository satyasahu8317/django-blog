# pyrefly: ignore [missing-import]
from django import forms
from .models import Comment, Post
# pyrefly: ignore [missing-import]
from django_summernote.widgets import SummernoteWidget



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category', 'image','body', 'status')
        widgets = {
            'body': SummernoteWidget(),
        }
