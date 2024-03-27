from django.shortcuts import render, redirect, get_object_or_404 
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TareaForm
from .usuario import Crearusuario
from .models import Tarea
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
# Create your views here/vistas
def home(request):
    return render(request, 'home.html')

def regis(request):
    
    if request.method == 'GET':
        return render(request, 'regis.html', {
        'form' : Crearusuario
        })
    else: #si el request metodo es post
        if request.POST['password1'] == request.POST['password2'] and len(request.POST['password1']) >= 6:
            try:
                #valida que si sea email
                validate_email(request.POST['email'])                
                #form = UserCreationForm(username.CharField(label='nombre de usuario'))
                user = User.objects.create_user(
                username=request.POST['email'],
                password=request.POST['password1']) 
                user.save() #lo guarda en bd
                login(request, user) #crea el cookie de sesion
                return redirect('tasks') #HttpResponse("user created")   
            except (ValidationError, IntegrityError): 
                return render(request, 'regis.html', {
                    'form' : Crearusuario,
                    "error": "Correo electrónico no valído o ya está en uso"
                })                           
    
        return render(request, 'regis.html', {
        'form' : Crearusuario,
        'error': "Contraseñas no coinciden o no tiene al menos 6 caracterés"
        })
       # HttpResponse("OSiris mal passw")
@login_required #proteje urls
def tarea(request):
    tareas = Tarea.objects.filter(user= request.user, fechacompletado__isnull=True) #fechacompletado__isnull=True q la liste si no compl
    return render(request, 'tasks.html', {'tareas': tareas})
@login_required
def tacompl(request):
    tareas = Tarea.objects.filter(user= request.user, fechacompletado__isnull=False).order_by('fechacompletado') #-??? se pone?
    return render(request, 'tacompl.html', {'tareas': tareas})
@login_required
def salir(request):
    logout(request) #quita cookie sesion
    return redirect('home')
@login_required
def salir2(request, tarea_id):
    logout(request) #quita cookie sesion
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
        'form' : AuthenticationForm
        })
    else:
        user = authenticate(request, username = request.POST['username'],
                            password = request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
        'form' : AuthenticationForm,
        'error': 'Nombre de usuario y contraseña no coinciden'
        })
        else:
            login(request, user)
            return redirect('tasks')
@login_required    
def crear_tarea(request):
    if request.method == 'GET':
        return render(request, 'crear_tarea.html',{
        'form' : TareaForm
        })
    else:
        try:
            form = TareaForm(request.POST) #le ponde los datos del form qse envia
            new_task = form.save(commit=False) #evita que se guarde
            new_task.user = request.user #usuario loggeado
            new_task.save()
            return redirect('tasks')
        except:
            return render (request, 'tasks.html', {
                    'error' : "tarea no sirve"
                })
            
@login_required            
def detalle_tarea(request, tarea_id):
    if request.method == 'GET':
        tarea = get_object_or_404(Tarea, pk=tarea_id, user=request.user)
        form = TareaForm
        return render(request, 'detarea.html', {'tarea': tarea, 'form': form})
    else: 
        try:
            tarea = get_object_or_404(Tarea, pk=tarea_id, user=request.user) 
            form = TareaForm(request.POST, instance=tarea)
            form.save()
            return redirect('tasks')
        except: ValueError
        return render(request, 'detarea.html', {'tarea': tarea, 'form': form, 
                                                'error': "No es posible actualizar"})
        
@login_required        
def borrar(request, tarea_id):
    tarea = get_object_or_404(Tarea, pk=tarea_id, user=request.user) 
    if request.method == 'POST':
        tarea.delete()
        return redirect('tasks')
@login_required    
def completa(request, tarea_id):
    tarea = get_object_or_404(Tarea, pk=tarea_id, user=request.user) 
    if request.method == 'POST':
        tarea.fechacompletado = timezone.now()
        tarea.save()
        return redirect('tasks')
        
        
        
            
        
    