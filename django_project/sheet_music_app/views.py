from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .models import Book
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


# Homepage view, registered users only
@login_required(login_url='login')
def home(request):
    return render(request, "home.html", {})

# User registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})