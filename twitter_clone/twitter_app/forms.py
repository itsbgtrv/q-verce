from django import forms
from .models import Post, Comment, Forum, News, Joblist

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ['text']

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['text', 'image'] 

class JoblistForm(forms.ModelForm):
    class Meta:
        model = Joblist
        fields = ['text', 'image']