from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignupForm, LoginForm
from profiles.models import StudentProfile


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('analytics:dashboard')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create empty profile
            StudentProfile.objects.create(
                user=user,
                full_name=f"{user.first_name} {user.last_name}".strip() or user.username,
                college='', branch='', year='1',
            )
            login(request, user)
            messages.success(request, "Welcome to HackTeam AI! Complete your profile to get started.")
            return redirect('profiles:edit')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('analytics:dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'analytics:dashboard')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('landing')
