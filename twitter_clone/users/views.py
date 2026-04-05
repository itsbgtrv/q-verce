from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm, EmailAuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

class CustomLoginView(LoginView):
    authentication_form = EmailAuthenticationForm
    template_name = 'users/login.html'

    success_url = reverse_lazy('home')


def logout_view(request):
    logout(request)
    return redirect('base')
