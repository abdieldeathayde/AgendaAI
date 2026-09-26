from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import LoginForm, UserRegistrationForm


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login realizado com sucesso.')
                return redirect('dashboard')
            form.add_error(None, 'Credenciais inválidas.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Cadastro realizado com sucesso! Faça login para continuar.')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form, 'title': 'Cadastro de usuário'})


def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu da aplicação.')
    return redirect('login')
