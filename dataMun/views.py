from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from .forms import *
from .decorators import *
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import openpyxl

import string

from django.forms.utils import ErrorList

def alphabet():
  return list(string.ascii_uppercase)

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
    return render(request, 'home.html',context)

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


    

def read_excel(tabla):
    errors=["None"]
    print(tabla)
    
    try:

        workbook = openpyxl.load_workbook(tabla)
    
        for sheet in workbook.worksheets:
            print("Saving week: " + sheet.title)
            crearPacientes =False
            try:
                year = (sheet.title).split(' ')[0]
                semana = (sheet.title).split(' ')[1]
                semana = Semana.objects.get(year=year,semana=semana)
                
                crearPacientes =False
                #print("zona obtained")
            except :
                semana =None

            
            if semana == None:
                try:
                    year = (sheet.title).split(' ')[0]
                    semana = (sheet.title).split(' ')[1]
                    semana = Semana(year=year,semana=semana)


                    semana.save(force_insert=True)
                    print("week added")
                    crearPacientes = True
                except :
                    print("error: week dont added correctly.")
                    error = [2,"(week dont added correctly.),"]
                    errors.append(error)
                    
                    crearPacientes =False
            
            if crearPacientes :
                letras = ['f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u']
                for i in range(0,6):
                    if i != 2 and i != 4:
                        print(alphabet()[i])
                        for num in range(1, sheet.max_row):
                            
                            celda = str(sheet[alphabet()[i] + str(num)].value)
                            """
                            try:
                                print("celda: " +alphabet()[i] + str(num) + " value: " + str(celda))
                            except:
                                print("celda: " +alphabet()[i] + str(num) + " value: none" )"""
                            
                            if i ==0:
                                if celda != 'None':
                                    if celda != "Z":
                                        try:
                                            zona = Zona.objects.get(codigo=int(celda))
                                            #print("zone exists")
                                        except :
                                            zona =None

                                        
                                        if zona == None:
                                            try:
                                                zona = Zona(codigo=int(celda))

                                                zona.save(force_insert=True)
                                                #print("zona added")
                                            except :
                                                pass
                                                #print("error: the zone dont created correctly.")
                                            
                            if i == 1:
                                if celda != 'None':
                                    if celda != "CS":
                                        if celda != "":
                                            try:
                                                centro = Centro.objects.get(codigo=int(celda))
                                                #print("centro obtained")
                                            except :
                                                centro =None

                                            
                                            if centro == None:
                                            
                                                try: 
                                                    
                                                    zona = Zona.objects.get(codigo=int(str(sheet["A"+ str(num)].value)))
                                                    
                                                    centro = Centro(codigo=int(celda),nombre=str(sheet["C"+ str(num)].value),zona=zona)
                                                    
                                                    centro.save(force_insert=True)
                                                    print("centro creado")
                                                except :
                                                    pass
                                                    #print("no anduvo")
                                                    
                            if i == 3:
                                if celda != 'None':
                                    if celda != "COD":
                                        if celda != "":
                                            diagnostico = None
                                            try:
                                                diagnostico = Diagnostico.objects.get(codigo=str(celda))
                                                #print("diagnostico obtained")
                                            except :
                                                diagnostico =None

                                            
                                            if diagnostico == None:
                                            
                                                try: 
                                                    
                                                    
                                                    
                                                    diagnostico = Diagnostico(codigo=str(celda),nombre=str(sheet["E"+ str(num)].value))
                                                    
                                                    diagnostico.save(force_insert=True)
                                                    #print("diagnostico creado")
                                                    diagnostico = Diagnostico.objects.get(codigo=str(celda))
                                                except :
                                                    #print("no anduvo crear el diagnostico")
                                                    pass
                                                
                            if i== 5:
                                if num != 1 and num != 2 and str(sheet["E"+ str(num)].value) != "TOTALES":
                                    try:
                                        diagnostico = Diagnostico.objects.get(codigo=str(sheet["D" + str(num)].value))
                                        #print("diagnostico obtained")
                                    except :
                                        print("error d")
                                        diagnostico =None
                                    try:
                                        centro = Centro.objects.get(codigo=int(str(sheet["B" + str(num)].value)))
                                        #print("centro obtained")
                                    except :
                                        print("error c")
                                        centro =None
                                    
                                    if centro != None and diagnostico  != None:
                                        for l in range(0,len(letras)):
                                            
                                            celda2 = str(sheet[letras[l] + str(num)].value)
                                            

                                            if celda2 != 'None':
                                                
                                                try: 
                                                    cant = int(celda2)
                                                
                                                    #print("se encontro una cantidad")
                                                    #print("cant " + str(cant))
                                                    for h in range(0,cant):
                                                        sexo = str(sheet[letras[l] + "2"].value)
                                                        if sexo == "F":

                                                            edad = str(sheet[letras[l-1] + "1"].value).strip(" años")
                                                        else:
                                                            edad = str(sheet[letras[l] + "1"].value).strip(" años")
                                                        edad = edad.strip(" año")
                                                        
                                                        #print("sexo " + sexo)
                                                        #print("edad " + edad)
                                                        try: 
                                                            paciente = Paciente(sexo=sexo,edad=edad,diagnostico=diagnostico,centro=centro,semana=semana)
                                                            paciente.save(force_insert=True)
                                                            #print("Paciente creado")
                                                        except :
                                                            pass
                                                            #print("nos se pudo crea al paciente")
                                                except :
                                                    pass
                                                    #print("No se encontro una cantidad")
    except:
        error = [1,"(File is not a zip file.),"]
        errors.append(error)
    return [tabla,errors]
                                
