#!/usr/bin/env python

import openpyxl
import string
from .models import *
import math


def alphabet():
    return list(string.ascii_lowercase)


def read_excel(archivo):
    errors = ["None"]
    print(archivo.tabla)

    zona = 0
    cod=0
    cs=0
    cname=""
    diag=""

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
            try:
                for row in sheet.iter_rows(values_only=True):
                    if row[4] != "Totales":
                        try:
                            zona = int(row[0])
                            cs = int(row[1])
                            cname = str(row[2])
                            cod = str(row[3])
                            diag = str(row[4])
                        except:
                            pass
                        if zona not in zonasCod:
                            nzona = Zona(codigo=zona)
                            nzona.save()
                            zonasCod.append(zona)
                        if cs not in centrosCod:
                            ozona = Zona.objects.get(codigo=zona)
                            ncentro = Centro(codigo=cs,nombre=cname,zona=ozona)
                            ncentro.save()
                            centrosCod.append(cs)
                        if cod not in diagnosticosCod:
                            ndiagnostico = Diagnostico(codigo=cod, nombre=diag)
                            ndiagnostico.save()
                            diagnosticosCod.append(cod)
                        try:
                            ocentro = Centro.objects.get(codigo=cs)
                            odiagnostico = Diagnostico.objects.get(codigo=cod)
                        except:
                            print("error de centro y diagnostico")
                            ocentro = None
                            odiagnostico = None

                        if ocentro != None and odiagnostico != None:
                            try:
                                for i in (0,len(letras)-1):
                                    sexo = ""
                                    edad = ""
                                    cant = 0

                                    if (i+1) % 2 != 0:
                                        sexo = "M"
                                        edad = str(sheet[letras[i] + "1"].value)
                                    else:
                                        sexo = "F"
                                        edad = str(sheet[letras[i-1] + "1"].value)

                                    edad = edad.strip(" años")
                                    edad = edad.strip(" año")
                                    npaciente = Paciente(sexo=sexo,edad=edad,cant_casos=cant,
                                                         diagnostico=odiagnostico,centro=ocentro,semana=semana)
                                    npaciente.save()
                            except:
                                print("Error creando el paciente")
            except:
                error = [1, "(File is not a zip file.),"]
                errors.append(error)
    return errors


class FuncionGrafico1():
    def __init__(self, media, year, rangoInferior, rangoSuperior):
        self.media = media
        self.year = year
        self.rangoInferior = rangoInferior
        self.rangoSuperior = rangoSuperior

    def __str__(self):
        return "media: " + str(self.media) + " year: " + str(self.year)


def funcionGrafico1(pacientes, diagnostico, yearInit, yearStop):
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
        casosPerSemana = []
        for semana in semanaYear:
            year = semana.year

            suma += pacientes.filter(semana=semana).count()
            casosPerSemana.append(pacientes.filter(semana=semana).count())

        casosPerYears.append(casosPerSemana)

        media = suma / len(semanaYear)
        medias.append(media)
    desviacionesEstandar = []
    suma = 0
    for media in medias:
        suma += media
    prom = suma / len(medias)

    for casosPerSemanas in casosPerYears:
        suma = 0

        for casosPerSemana in casosPerSemanas:
            suma += (casosPerSemana - prom) ** 2

        desviacionEstandar = math.sqrt(suma / len(casosPerSemanas))
        desviacionesEstandar.append(desviacionEstandar)

    for desviacionEstandar in desviacionesEstandar:
        rangoInferior = prom - (3.18 * desviacionEstandar / math.sqrt(len(semanasYear)))
        rangoSuperior = prom + (3.18 * desviacionEstandar / math.sqrt(len(semanasYear)))

        funcion = FuncionGrafico1(media, year, rangoInferior, rangoSuperior)
        funcionesGrafico1.append(funcion)

    return funcionesGrafico1
