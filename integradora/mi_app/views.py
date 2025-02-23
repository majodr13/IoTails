from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from .forms import RegistroUsuarioForm
from django.contrib.auth.hashers import make_password
import pymongo
from django.contrib.auth.decorators import login_required

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["IoTails"]
users_collection = db["users"]

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(f"Intentando autenticar: {username} con contraseña: {password}")  # Mensaje de depuración
        user = authenticate(request, username=username, password=password)
        
        if user is not None:  # Verifica si el usuario existe
            login(request, user)  # Inicia sesión
            return redirect('main')  # Redirige al main si el usuario existe
        else:
            error_message = "El usuario no existe o la contraseña es incorrecta."
            return render(request, 'login.html', {'error_message': error_message})
    
    return render(request, 'login.html')

def register_view(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            existing_user = users_collection.find_one({"username": username})
            if existing_user:
                return HttpResponse("El usuario ya existe", status=400)

            hashed_password = make_password(password)

            users_collection.insert_one({
                "username": username,
                "email": email,
                "password": hashed_password,
            })

            return redirect("login")

    else:
        form = RegistroUsuarioForm()

    return render(request, "register.html", {"form": form})

def main_view(request):
    return render(request, 'main.html', {"user": request.user})  

def home_view(request):
    return render(request, 'home.html')
