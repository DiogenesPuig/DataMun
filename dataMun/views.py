from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from .forms import *
from .decorators import *
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
import openpyxl
from .script import *
import string

from django.forms.utils import ErrorList
import datetime


# Create your views here.




@login_required()
def perfilView(request):
    
    return render(request, "perfil.html")



def logoutView(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("home")


@unauthenticated_user
def loginView(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login Exitoso")
            try:
                return redirect(request.POST.get('next'))
            except:
                return redirect('home')
        else:
            messages.error(request, "Usuario o Contraseña Incorrecta")
            
            return render(request, 'login.html', context)

    return render(request, 'login.html', context)


@unauthenticated_user
def registerView(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, "Account was created for " + username)
            return redirect('login')
    context = {
        'form': form
    }
    return render(request, 'register.html', context)





class PaceintePorDiagnostico():
    def __init__(self,cantPacientePorDiagnostico,diagnostico):
        self.cantPacientePorDiagnostico = cantPacientePorDiagnostico
        self.diagnostico = diagnostico


def homeView(request):
    pacientes = Paciente.objects.all()
    pacientesRec = []
    
    year = datetime.datetime.now().year
    semanas = Semana.objects.filter(year=year)
    maxSem = semanas[0]
    for semana in semanas:
        
        
        if semana.semana > maxSem.semana:
            maxSem = semana
    pacientesRec = Paciente.objects.filter(semana=maxSem)

    
    diagnosticos = Diagnostico.objects.all()
    maxDiagnosticos =[]
    cantPacientesPorDiagnostico = []
    for diagnostico in diagnosticos:
        cantDiagn = len(pacientesRec.filter(diagnostico=diagnostico))
        if cantDiagn != 0 and "TOTALES" not in diagnostico.nombre :
            maxDiagnosticos.append(diagnostico)
            cantPacientesPorDiagnostico.append(cantDiagn)
        
    
    
    n = len(maxDiagnosticos)
    print(str(n))
    # Traverse through all array elements
    max = 0
    for i in range(n-1):
    # range(n) also work but outer loop will repeat one time more than needed.
  
        # Last i elements are already in place
        
        for j in range(0, n-i-1):
  
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if cantPacientesPorDiagnostico[j] <  cantPacientesPorDiagnostico[j + 1] :
                l = maxDiagnosticos[j]
                maxDiagnosticos[j] = maxDiagnosticos[j + 1]
                maxDiagnosticos[j + 1] = l 
                l = cantPacientesPorDiagnostico[j]
                cantPacientesPorDiagnostico[j] = cantPacientesPorDiagnostico[j + 1]
                cantPacientesPorDiagnostico[j + 1] = l 
        if i == 50:
            break
                
                
            
    
    pacientePorDiagnosticos = []
    for l in range(0,len(maxDiagnosticos)):
        pacientePorDiagnostico = PaceintePorDiagnostico(diagnostico=maxDiagnosticos[l],cantPacientePorDiagnostico=cantPacientesPorDiagnostico[l])
        pacientePorDiagnosticos.append(pacientePorDiagnostico)

    paginator = Paginator(pacientePorDiagnosticos,50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'semana':maxSem,
        'pacientePorDiagnosticos':page_obj,
        
    }
    return render(request, 'home.html',context)



def diagnosticView(request,codigo_diagnostic):
    diagnostico = Diagnostico.objects.get(codigo=codigo_diagnostic)
    pacientes = Paciente.objects.all()
    medias = funcionGrafico1(pacientes,diagnostico,0,2022)
    context = {
        'medias':medias,
        'diagnostico':diagnostico
    }
    return render(request, 'diagnostic.html',context)




@login_required()
def uploadFileView(request):
    form = CreateArchivoForm()
    if request.method == "POST": # If the form has been submitted...
        
         # All validation rules pass
        form = CreateArchivoForm(request.POST, request.FILES)
        if form.is_valid():
            tabla = request.FILES["tabla"]
            archivo = form.save()

            success  = read_excel(request.FILES["tabla"])
            
            if len(success[1]) != 1:
                archivo = Archivo.objects.get(pk=archivo.id)
                archivo.delete()
                for error in success[1]:
                    if error[0] == 1:

                        form._errors["tabla"] = ErrorList([u" El archivo subido debe ser excel."])
                    if error[0] == 2:
                    
                        form._errors["tabla"] = ErrorList([u" Revisa que el titulo de la hoja este correcto con su año y semana"])
                    
                    context = {
                        'form':form
                    }

                
                return render(request, 'uploadFile.html',context)
            messages.success(request, "El archivo " + str(archivo.tabla) + ' fue agregado')
            return redirect('home') ## redirects to aliquot page ordered by the most recent
        
        

    else:
        form = CreateArchivoForm() # An unbound form
        
    context = {
        'form':form
    }
    return render(request, 'uploadFile.html',context)


    

