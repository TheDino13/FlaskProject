from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages

# Regiser View
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatic login after registration
            messages.success(request, "Registration successful!")
            print(f"User registered: {user.username}")
            return redirect('home')  # Redirecting to home page
        else:
            messages.error(request, "Error in the registration form.")
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

# Log In View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Welcome back!")
            print(f"User logged in: {user.username}")
            return redirect('home')
        else:
            messages.error(request, "Incorrect login or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

# Log Out View
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "See You later!")
        return redirect('home')
