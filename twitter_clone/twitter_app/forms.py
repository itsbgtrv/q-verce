from django import forms
from .models import Post, Comment, Forum, News, Joblist, Category

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # Добавил subtitle и category, чтобы пользователь мог их выбрать
        fields = ['title', 'subtitle', 'category', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Краткое описание'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Заголовок',
            'subtitle': 'Подзаголовок',
            'category': 'Категория',
            'content': 'Текст поста',
            'image': 'Изображение',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'image']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Напишите комментарий...', 
                'rows': 3
            }),
        }
        labels = {'text': ''}

class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ваше сообщение в форуме', 'rows': 4}),
        }
        labels = {'text': 'Сообщение'}

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'text', 'image'] # Добавил title, так как в модели он есть
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Заголовок новости',
            'text': 'Текст новости',
        }

class JoblistForm(forms.ModelForm):
    class Meta:
        model = Joblist
        fields = ['text', 'image']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание вакансии', 'rows': 5}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'text': 'Требования и описание',
            'image': 'Логотип или фото',
        }