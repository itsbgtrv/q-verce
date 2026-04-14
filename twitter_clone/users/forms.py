from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    # Указываем явно, что мы используем нашу модель
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'username')

    # Это важно: если ты хочешь, чтобы email был обязательным и проверялся как email
    email = forms.EmailField(required=True)



class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email')

