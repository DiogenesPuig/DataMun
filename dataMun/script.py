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

    codigo=0
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
            i = 0
            for row in sheet.iter_rows(values_only=True):
                for cell in row:
                    if i == 0:
                        print("0")
                        try:
                            codigo = int(cell)
                        except:
                            pass
                        if codigo not in zonasCod:
                            try:
                                zona = Zona(codigo=codigo)
                                zona.save(force_insert=True)
                                zonasCod.append(codigo)
                            except:
                                pass
                    elif i == 1:
                        print("1")
                        try:
                            codigo = int(cell)
                        except:
                            pass
                        if codigo not in centrosCod:
                            try:
                                zona = Zona.objects.get(codigo=int(str(row[1])))
                                new_centro = Centro(codigo=codigo,nombre=row[2],zona=zona)
                                new_centro.save(force_insert=True)
                                centrosCod.append(int(cell))
                            except:
                                pass
                    elif i == 3:
                        print("3")
                        try:
                            codigo = str(cell)
                        except:
                            pass
                        if codigo not in diagnosticosCod and codigo != 'None':
                            try:
                                new_diagnostico = Diagnostico(codigo=codigo,nombre=str(row[4]))
                                new_diagnostico.save(force_insert=True)
                                diagnosticosCod.append(str(cell))
                            except:
                                pass
                    elif i == 5:
                        print("5")
                        if row[4] != "TOTALES":
                            try:
                                diagnostico = Diagnostico.objects.get(codigo=row[3])
                            except:
                                diagnostico = None
                            try:
                                centro = Centro.objects.get(codigo=row[1])
                            except:
                                centro = None
                            if centro != None and diagnostico != None:
                                for l in range(0, len(letras)):
                                    try:
                                        cant = int(cell)

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

                                        # print("sexo " + sexo)
                                        # print("edad " + edad)
                                        try:
                                            paciente = Paciente(sexo=sexo, edad=edad,
                                                                diagnostico=diagnostico, centro=centro,
                                                                semana=semana, cant_casos=cant)
                                            paciente.save(force_insert=True)
                                            # print("Paciente creado")
                                        except:
                                            pass
                                            print("nos se pudo crea al paciente")
                                    except:
                                        pass
                i+=1

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
