from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponse, JsonResponse
from .forms import RegistroMascotaForm, RegistroUsuarioForm
import pymongo
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json
from .db_con import pets_collection
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SensorData
from .serializers import SensorDataSerializer
from django.utils.timezone import now

client = pymongo.MongoClient("mongodb+srv://IoTails:IoTails1234@iot.gcez4.mongodb.net/")
db = client["IoTails"]
users_collection = db["users"]
pets_collection = db["pets"]
sensor_collection = db["door"]
resumen_collection = db["sensors"]

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
            return JsonResponse({"error": str(form.errors)}, status=400)

    return render(request, "form.html", {"form": RegistroMascotaForm()})

@login_required
def profile_view(request):
    pets = list(pets_collection.find({})) 
    return render(request, 'perfil.html', {"pets": pets, "user": request.user})

def mapa_views(request):
    return render(request, 'mapa.html')

@login_required
def cuidados_views(request):
    datos_sensores = SensorData.objects.all().order_by('-fecha')[:10]
    sensor_docs = []
    for d in datos_sensores:
        sensor_docs.append({
            "temperatura": d.temperatura,
            "humedad": d.humedad,
            "estado_puerta": d.estado_puerta,
            "fecha": d.fecha.strftime("%Y-%m-%d %H:%M:%S"),
        })
    if sensor_docs:
        sensor_collection.insert_many(sensor_docs)

    return render(request, "cuidados.html", {"datos_sensores": datos_sensores})

@api_view(['POST'])
def api_cuidados(request):
    if not request.data:
        return Response({"error": "No se enviaron datos"}, status=400)

    data = {
        "temperatura": request.data.get("temperatura"),
        "humedad": request.data.get("humedad"),
        "estado_puerta": request.data.get("estado_puerta"),
        "bpm": request.data.get("bpm"),
        "spo2": request.data.get("spo2"),
    }

    serializer = SensorDataSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        try:
            sensor_collection.insert_one({
                "temperatura": data["temperatura"],
                "humedad": data["humedad"],
                "estado_puerta": data["estado_puerta"],
                "fecha": now().strftime("%Y-%m-%d %H:%M:%S")
            })
        except Exception as e:
            print("Error MongoDB:", e)

        return Response({"mensaje": "Datos guardados correctamente"}, status=201)

    return Response(serializer.errors, status=400)

def obtener_datos_sensores(request):
    datos = SensorData.objects.all().order_by('-fecha')[:10]
    datos_list = []
    for d in datos:
        datos_list.append({
            "temperatura": d.temperatura,
            "humedad": d.humedad,
            "estado_puerta": d.estado_puerta,
            "fecha": d.fecha.strftime("%d/%m/%Y, %I:%M:%S %p"),
        })
    return JsonResponse({"datos": datos_list}, safe=False)

datos_esp32 = {}

@csrf_exempt
def recibir_datos_resumen(request):
    global datos_esp32
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            lat = data.get('latitud')
            lon = data.get('longitud')

            ubicacion = "En casa" if not lat or not lon or lat == "0.0" or lon == "0.0" else f"Lat: {lat}, Lon: {lon}"

            datos_esp32 = {
                "bpm": data.get('bpm'),
                "spo2": data.get('spo2'),
                "ubicacion": ubicacion
            }

            resumen_collection.insert_one({
                "bpm": datos_esp32["bpm"],
                "spo2": datos_esp32["spo2"],
                "ubicacion": datos_esp32["ubicacion"],
                "fecha": now().strftime("%Y-%m-%d %H:%M:%S")
            })

            return JsonResponse({"status": "success"}, status=201)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    else:
        return JsonResponse({"status": "Método no permitido"}, status=405)

def resumen_view(request):
    datos = datos_esp32 if datos_esp32 else {}
    return render(request, 'resumen.html', {"datos": datos})