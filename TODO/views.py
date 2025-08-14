from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

# Authentication Views
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, 'Account created! Please login.')
            return redirect('login')
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


# Task Views
@login_required(login_url='login')
def home(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Task.objects.create(title=title, user=request.user)
        return redirect('home')

    tasks = Task.objects.filter(user=request.user, completed=False)
    completed_tasks = Task.objects.filter(user=request.user, completed=True)
    return render(request, 'home.html', {
        'tasks': tasks,
        'completed_tasks': completed_tasks
    })

@login_required(login_url='login')
def mark_done(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = True
    task.save()
    return redirect('home')

@login_required(login_url='login')
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('home')

@login_required(login_url='login')
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            task.title = title
            task.save()
    return redirect('home')  # redirect back to main page
