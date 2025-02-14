from django.shortcuts import render

def main_view(request):
    return render(request, 'main.html')

def login_view(request):
    return render(request, 'login.html')  

def register_view(request):
    return render(request, 'register.html')
