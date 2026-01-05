from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Todo


# LOGIN VIEW
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return redirect('register')
    return render(request, 'login.html')

# REGISTER VIEW
def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            return render(request, "register.html", {"error": "Passwords do not match"})

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Username already exists"})

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect("dashboard") 

    return render(request, "register.html")


# DASHBOARD
def dashboard(request):
    if request.method == "POST":
        title = request.POST['title']
        Todo.objects.create(user=request.user, title=title)
    todos = Todo.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'todos': todos})


@login_required
def dashboard(request):
    q = request.GET.get("q", "") 
    todos = Todo.objects.filter(user=request.user, title__icontains=q)
    return render(request, "dashboard.html", {"todos": todos})


@login_required
def add_todo(request):
    if request.method == "POST":
        title = request.POST["title"]
        Todo.objects.create(user=request.user, title=title)
        return redirect("dashboard")
    return render(request, "add_todo.html")


@login_required
def edit_todo(request, id):
    todo = get_object_or_404(Todo, id=id, user=request.user)

    if request.method == "POST":
        todo.title = request.POST["title"]
        todo.save()
        return redirect("dashboard")

    return render(request, "edit_todo.html", {"todo": todo})


@login_required
def delete_todo(request, id):
    todo = get_object_or_404(Todo, id=id, user=request.user)
    todo.delete()
    return redirect("dashboard")


def logout_view(request):
    logout(request)          # clears session
    return redirect("login") 