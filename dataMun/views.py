from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from .forms import *
from .decorators import *
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from .script import *
from .filters import *
from django.conf import settings

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



def homeView(request):
    
    context = {
        
    }
    return render(request, 'home.html',)






class PaceintePorDiagnostico():
    def __init__(self,cantPacientePorDiagnostico,diagnostico):
        self.cantPacientePorDiagnostico = cantPacientePorDiagnostico
        self.diagnostico = diagnostico

@user_passes_test(lambda u:u.is_staff)
def diagnosticosView(request):

    
    try:
    
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
            if  "TOTALES" not in diagnostico.nombre :
                pac = pacientesRec.filter(diagnostico=diagnostico)
                cantDiagn = 0
                for i in pac:
                    cantDiagn += i.cant_casos
                if cantDiagn != 0 :
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
    except:
        pass
        context = {}
    return render(request, 'diagnosticos.html',context)


@user_passes_test(lambda u:u.is_staff)
def diagnosticView(request,codigo_diagnostic):
    
    
    diagnostico = Diagnostico.objects.get(codigo=codigo_diagnostic)
    pacientes = Paciente.objects.all()
   
    semanas =  Semana.objects.all()
    p = PacienteFilter(request.GET, queryset=pacientes)
    s = SemanaFilter(request.GET, queryset=semanas)
    try:
        year = int(request.GET.get('year__lt'))
    except:
        year = 0
    if year == 0:
        year = 2021

    
    centrosName = []
    centros = []
    centro = ""
    suma = 0
    pacientes = p.qs.filter(diagnostico=diagnostico).order_by("centro")
    for pac in pacientes:
        if pac.centro not in centrosName:
            if pac.centro.nombre == centro:
                suma += 1
            else:
            
                centrosName.append(centro)
                n = 'centro ' +centro
                co = {
                    'nombre': n,
                    'cases':suma,
                    'cod':pac.centro.codigo,
                }
                
                centros.append(co)
                
                centro = pac.centro.nombre
            
                suma = 0
        if len(centrosName) >= 20:
            break
    print(len(centros))
    medias = funcionGrafico1(p.qs,diagnostico,s.qs)
    cuartiles = funcionGrafico2(p.qs,diagnostico,s.qs,year,2)
    context = {
        'medias':medias,
        'cuartiles':cuartiles,
        'diagnostico':diagnostico,
        'filterP': p,
        'filterS': s,
        'google_api_key':settings.APY_KEY,
        'centros': centros,
    }
    return render(request, 'diagnostic.html',context)




@user_passes_test(lambda u:u.is_staff)
def uploadFileView(request):
    form = CreateArchivoForm()
    if request.method == "POST": # If the form has been submitted...
        
         # All validation rules pass
        form = CreateArchivoForm(request.POST, request.FILES)
        if form.is_valid():
            tabla = request.FILES["tabla"]
            archivo = form.save()
            archivo = Archivo.objects.get(pk=archivo.id)
            success = read_excel(archivo)
            
            
            
            if len(success) != 1:
                archivo = Archivo.objects.get(pk=archivo.id)
                archivo.delete()
                for error in success:
                    if error[0] == 1:

                        form._errors["tabla"] = ErrorList([u" El archivo subido debe ser excel."])
                    if error[0] == 2:
                    
                        form._errors["tabla"] = ErrorList([u" Revisa que el titulo de la hoja este correcto con su año y semana"])
                    
                    context = {
                        'form':form
                    }

                
                return render(request, 'uploadFile.html',context)
            messages.success(request, "El archivo " + str(archivo.tabla) + ' fue agregado')
            return redirect('diagnosticos') ## redirects to aliquot page ordered by the most recent
        
        

    else:
        form = CreateArchivoForm() # An unbound form
        
    context = {
        'form':form
    }
    return render(request, 'uploadFile.html',context)


    

