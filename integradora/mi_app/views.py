from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse, JsonResponse
from .forms import RegistroMascotaForm, RegistroUsuarioForm
from django.contrib.auth.hashers import make_password
import pymongo
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .db_con import pets_collection
from django.conf import settings

client = pymongo.MongoClient("mongodb+srv://IoTails:IoTails1234@iot.gcez4.mongodb.net/")
db = client["IoTails"]
users_collection = db["users"]

class MongoUser:
    def __init__(self, user_data):
        self.email = user_data['email']
        self.first_name = user_data.get('first_name', '')
        self.last_name = user_data.get('last_name', '')
        self.password = user_data['password']
        self.is_authenticated = True 

    def __str__(self):
        return self.email

def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user_data = users_collection.find_one({"email": email})

        if user_data and check_password(password, user_data["password"]):  
            user, created = User.objects.get_or_create(username=email)
            login(request, user)
            return redirect("main")  

        elif not user_data:
            messages.error(request, "Usuario no registrado.")
            return render(request, "login.html")

        messages.error(request, "Credenciales incorrectas.")
        return render(request, "login.html")

    return render(request, "login.html")

def register_view(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"] 
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # Revisar si el usuario ya existe
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
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'main.html')

def home_view(request):
    return render(request, 'home.html')

def form_view(request):
    return render(request, "form.html")

def registrar_mascota(request):
    if request.method == "POST":
        print("request.POST:", request.POST.dict())  
        print("request.FILES:", request.FILES) 

        form = RegistroMascotaForm(request.POST, request.FILES)
        if form.is_valid():
            mascota_data = {
                "nombre": form.cleaned_data["nombre"],
                "edad": form.cleaned_data["petAge"],  
                "peso": form.cleaned_data["weight"], 
                "tipo": form.cleaned_data["tipo"],
                "tamaño": form.cleaned_data["petSize"], 
                "problemasMed": form.cleaned_data["problemasMed"],
                "dueño": form.cleaned_data["ownerEmail"], 
                "imagen": request.FILES.get("pic", None),  
            }
            
            pets_collection.insert_one(mascota_data)
            return JsonResponse({"message": "Mascota registrada exitosamente"}, status=201)
        else:
            print("Errores en el formulario:", form.errors)  
            return JsonResponse({"error": str(form.errors)}, status=400)

    return render(request, "form.html", {"form": RegistroMascotaForm()})

@login_required
def profile_view(request):
    pets = list(settings.PETS_COLLECTION.find({})) 

    return render(request, 'perfil.html', {"pets": pets, "user": request.user})


def mapa_views(request):
    return render(request, 'mapa.html')

def cuidados_views(request):
    return render(request, "cuidados.html")

