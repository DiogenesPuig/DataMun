#!/usr/bin/env python

import openpyxl
import string
from .models import *
import math
def alphabet():
  return list(string.ascii_lowercase)


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
                                
class FuncionGrafico1():
    def __init__(self,media, year, rangoInferior,rangoSuperior):
        self.media = media
        self.year = year
        self.rangoInferior= rangoInferior
        self.rangoSuperior= rangoSuperior
        
    def __str__(self):
        return "media: " + str(self.media) + " year: " + str(self.year)

    
def funcionGrafico1(pacientes,diagnostico,yearInit,yearStop):
    semanas = Semana.objects.filter(year__gte=yearInit).filter(year__lt=yearStop).order_by("year")
    
    semanasYear = []
    semanaYear = []
    year = semanas[0].year
    for semana in semanas: 
        
        if semana.year != year:
            semanasYear.append(semanaYear)
            
            semanaYear = []
       
        semanaYear.append(semana)
        
        year = semana.year
    if len(semanasYear) == 0:
        semanasYear.append(semanaYear)



    pacientes = pacientes.filter(diagnostico=diagnostico)
    casosPerYears = []
    funcionesGrafico1 = []
    medias = []
    for semanaYear in semanasYear:
        
        media = 0
        suma = 0
        year = 0
        casosPerSemana= []
        for semana in semanaYear:
            year = semana.year
             

            suma += pacientes.filter(semana=semana).count()
            casosPerSemana.append(pacientes.filter(semana=semana).count())
            
        casosPerYears.append(casosPerSemana)
           

        media = suma / len(semanaYear)
        medias.append(media)
    desviacionesEstandar= []
    suma = 0 
    for media in medias:
        suma+= media
    prom= suma/len(medias)

    for casosPerSemanas in casosPerYears:
        suma=0

        for casosPerSemana in casosPerSemanas:
            suma += (casosPerSemana - prom)**2
            
        desviacionEstandar = math.sqrt(suma/len(casosPerSemanas))
        desviacionesEstandar.append(desviacionEstandar)

        
        
    for desviacionEstandar in desviacionesEstandar:
        rangoInferior = prom - (3.18 * desviacionEstandar/math.sqrt(len(semanasYear)))
        rangoSuperior = prom + (3.18 * desviacionEstandar/math.sqrt(len(semanasYear)))
        
        funcion = FuncionGrafico1(media,year,rangoInferior,rangoSuperior)
        funcionesGrafico1.append(funcion)
        
    



    

    
    return funcionesGrafico1
    
    
    
    
