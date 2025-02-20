from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegistroUsuarioForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from bson.objectid import ObjectId
from .models import person_collection
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    return render(request, 'login.html')

def register_view(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            existing_user = person_collection.find_one({"username": username})
            if existing_user:
                return HttpResponse("El usuario ya existe", status=400)

            hashed_password = make_password(password)

            person_collection.insert_one({
                "_id": ObjectId(),
                "username": username,
                "email": email,
                "password": hashed_password,
            })

            return redirect("login")

    else:
        form = RegistroUsuarioForm()

    return render(request, "register.html", {"form": form})

def main_view(request):
    return render(request, 'main.html')

    