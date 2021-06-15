#!/usr/bin/env python

import openpyxl
import string
from .models import *
import math
import random

def alphabet():
    return list(string.ascii_lowercase)


def read_excel(archivo):
    errors = ["None"]
    print(archivo.tabla)

    try:

        workbook = openpyxl.load_workbook(archivo.tabla)
        alphabe = alphabet()
        letras = ['f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u']
        centros = Centro.objects.all()
        centrosCod = []
        for i in centros:
            centrosCod.append(i.codigo)

        diagnosticos = Diagnostico.objects.all()
        diagnosticosCod = []
        for i in diagnosticos:
            diagnosticosCod.append(i.codigo)

        zonas = Zona.objects.all()
        zonasCod = []
        for i in zonas:
            zonasCod.append(i.codigo)

        for sheet in workbook.worksheets:
            print("Saving week: " + sheet.title)
            crearPacientes = False
            try:
                year = (sheet.title).split(' ')[0]
                semana = (sheet.title).split(' ')[1]
                semana = Semana.objects.get(year=year, semana=semana)

                crearPacientes = False
                # print("zona obtained")
            except:
                semana = None

            if semana == None:
                try:
                    year = (sheet.title).split(' ')[0]
                    semana = (sheet.title).split(' ')[1]
                    semana = Semana(year=year, semana=semana, archivo=archivo)

                    semana.save(force_insert=True)
                    semana = (sheet.title).split(' ')[1]
                    semana = Semana.objects.get(year=year, semana=semana)
                    print("week added")
                    crearPacientes = True
                except:
                    print("error: week dont added correctly.")
                    error = [2, "(week dont added correctly.),"]
                    errors.append(error)

                    crearPacientes = False

            if crearPacientes:

                for i in range(0, 6):
                    if i != 2 and i != 4:
                        print(alphabe[i])
                        for num in range(1, sheet.max_row):
                            if num != 1 and num != 2:
                                celda = str(sheet[alphabe[i] + str(num)].value)
                                """
                                try:
                                    print("celda: " +alphabet()[i] + str(num) + " value: " + str(celda))
                                except:
                                    print("celda: " +alphabet()[i] + str(num) + " value: none" )"""

                                if i == 0:
                                    try:
                                        codigo = int(celda)
                                    except:
                                        pass
                                    if codigo not in zonasCod:
                                        try:
                                            zona = Zona(codigo=int(celda))

                                            zona.save(force_insert=True)
                                            zonasCod.append(int(celda))
                                            # print("zona added")
                                        except:
                                            pass
                                            # print("error: the zone dont created correctly.")

                                elif i == 1:
                                    try:
                                        codigo = int(celda)
                                    except:
                                        pass
                                    if codigo not in centrosCod:

                                        try:

                                            zona = Zona.objects.get(codigo=int(str(sheet["A" + str(num)].value)))

                                            centro = Centro(codigo=int(celda), nombre=str(sheet["C" + str(num)].value),
                                                            zona=zona)

                                            centro.save(force_insert=True)
                                            centrosCod.append(int(celda))
                                            # print("centro creado")
                                        except:
                                            pass
                                            # print("no anduvo")

                                elif i == 3:
                                    try:
                                        codigo = str(celda)
                                    except:
                                        pass
                                    if codigo not in diagnosticosCod and codigo != 'None':

                                        try:

                                            diagnostico = Diagnostico(codigo=str(celda),
                                                                      nombre=str(sheet["E" + str(num)].value))

                                            diagnostico.save(force_insert=True)
                                            # print("diagnostico creado")
                                            diagnosticosCod.append(str(celda))

                                        except:
                                            # print("no anduvo crear el diagnostico")
                                            pass

                                elif i == 5:
                                    if str(sheet["E" + str(num)].value) != "TOTALES":
                                        try:
                                            diagnostico = Diagnostico.objects.get(
                                                codigo=str(sheet["D" + str(num)].value))
                                            # print("diagnostico obtained")
                                        except:
                                            print("error d")
                                            diagnostico = None
                                        try:
                                            centro = Centro.objects.get(codigo=int(str(sheet["B" + str(num)].value)))
                                            # print("centro obtained")
                                        except:
                                            print("error c")
                                            centro = None

                                        if centro != None and diagnostico != None:
                                            for l in range(0, len(letras)):

                                                celda2 = str(sheet[letras[l] + str(num)].value)

                                                try:
                                                    cant = int(celda2)

                                                    # print("se encontro una cantidad")
                                                    # print("cant " + str(cant))
                                                    sexo = ""
                                                    edad = ""
                                                    if (l + 1) % 2 != 0:
                                                        sexo = "M"
                                                        edad = str(sheet[letras[l] + "1"].value)
                                                    else:

                                                        edad = str(sheet[letras[l - 1] + "1"].value)
                                                        sexo = "F"

                                                    edad = edad.strip(" años")
                                                    edad = edad.strip(" año")
                                                    
                                                    cant = random.randint(1, cant*2)
                                                    
                                                    # print("sexo " + sexo)
                                                    # print("edad " + edad)
                                                    try:
                                                        paciente = Paciente(sexo=sexo, edad=edad,
                                                                            diagnostico=diagnostico, centro=centro,
                                                                            semana=semana,cant_casos=cant)
                                                        paciente.save(force_insert=True)
                                                        # print("Paciente creado")
                                                    except:
                                                        pass
                                                        print("nos se pudo crea al paciente")
                                                except:
                                                    pass
                                                    # print("No se encontro una cantidad")
    except:
        error = [1, "(File is not a zip file.),"]
        errors.append(error)
    return errors


class FuncionGrafico1():
    def __init__(self, media, semana, rangoInferior, rangoSuperior,cant_casos):
        self.media = media
        self.semana = semana
        self.rangoInferior = rangoInferior
        self.rangoSuperior = rangoSuperior
        self.cant_casos = cant_casos

    def __str__(self):
        return "media: " + str(self.media) + " year: " + str(self.year)


def funcionGrafico1(pacientes, diagnostico, semanas ):
    
    
    pacientes = pacientes.filter(diagnostico=diagnostico)

    medias = [0] * 52
    desviacionesEstandar = [0] * 52
    cantidadesSemana = [0] * 52
    cantidadesCasos = [0] * 52
    
    for i in range(len(medias)):
        cantSemanas = 0
        cantidadCasos = 0 
        sumas = []
        
        for semana in semanas:
            if semana.semana == i+1:
                pac = pacientes.filter(semana=semana)
                
                for p in pac:
                    
                    cantidadCasos += p.cant_casos
                sumas.append(cantidadCasos)
                cantSemanas += 1

            
        if cantidadCasos != 0:
            cantidadesCasos[i] = cantidadCasos
            media = cantidadCasos / cantSemanas
            
            medias[i] = media
            desviacionEstandar = 0 
            if len(sumas) != 1:
                suma2 = 0 
                for cantidadCasos in sumas:
                    suma2 += (cantidadCasos-media)**2
                desviacionEstandar = math.sqrt(suma2 / len(sumas))
                
            desviacionesEstandar[i] = desviacionEstandar

            cantidadesSemana[i] = cantSemanas

    cantidadCasos =  0
    for media in medias:
        cantidadCasos += media

    prom = cantidadCasos/len(medias)


    funcionesGrafico1 = []
    for i in range(len(desviacionesEstandar)):
        rangoInferior = 0
        rangoSuperior = 0
        if cantidadesSemana[i] !=0:
            rangoInferior = medias[i] - (3.18 * desviacionesEstandar[i] / math.sqrt(cantidadesSemana[i]))
            rangoSuperior = medias[i] + (3.18 * desviacionesEstandar[i] / math.sqrt(cantidadesSemana[i]))
        

        funcion = FuncionGrafico1(medias[i],i+1, rangoInferior, rangoSuperior,cantidadesCasos[i])
        funcionesGrafico1.append(funcion)

    return funcionesGrafico1


class PuntoGrafico2():
    def __init__(self,c1,c2,c3,casos,semana):
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.casos = casos
        self.semana  = semana
def funcionGrafico2(pacientes, diagnostico, semanas,year, cantYear):
    #idk la verdad
    semanas = semanas.order_by("year")

    pacientes = pacientes.filter(diagnostico=diagnostico)
    suma = 0
    if cantYear % 2 != 0:
        suma = -1
    c = [(cantYear+suma)*1 / 4,(cantYear+suma)*2 / 4,(cantYear+suma)*3 / 4]

    
    
    
    puntosGrafico2 = [ ]
    cantidadesCasos = [0] * 52
    for o in range(52):
        puntos=[]
        cantidadesCasos = [0.0] * (cantYear)
        for i in range(len(cantidadesCasos)):

            cantidadCasos = 0 
            
            
            for semana in semanas:
                
                if semana.year == year-(i+1):
                    if semana.semana ==  o+1:
                        pac = pacientes.filter(semana=semana)
                        
                        for p in pac:
                            
                            cantidadCasos += p.cant_casos
            if cantidadCasos != 0:
                cantidadesCasos[i] = float(cantidadCasos)
                
        
        n = len(  cantidadesCasos )
        for j in range(n-1): # range(n) also work but outer loop will repeat one time more than 
            for j in range(0, n-i-1):
                if cantidadesCasos[j] >  cantidadesCasos[j + 1] :
                    
                    l = cantidadesCasos[j]
                    cantidadesCasos[j] = cantidadesCasos[j + 1]
                    cantidadesCasos[j + 1] = l 
        
        for r in range(len(c)):


            puntos.append(cantidadesCasos[int(c[r])])
        
    
        cantidadCasosPerSemana = 0 
        
        
        for semana in semanas:
            if semana.semana == o+1:
                pac = pacientes.filter(semana=semana)
                
                for p in pac:
                    
                    cantidadCasosPerSemana += p.cant_casos
       
        
        punto = PuntoGrafico2(puntos[0],puntos[1],puntos[2],cantidadCasosPerSemana,o+1)
        puntosGrafico2.append(punto)

    return puntosGrafico2
    