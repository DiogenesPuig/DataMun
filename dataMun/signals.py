from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import *
from .forms import *


import openpyxl

import string
import datetime

def alphabet():
  return list(string.ascii_uppercase)


@receiver(post_save,sender=Archivo)
def CreateSemana(sender, instance, created, **kwargs):
    archivo = Archivo()
    if created:
        
        print(instance.tabla )

        workbook = openpyxl.load_workbook(instance.tabla)
        for sheet in workbook.worksheets:
            print("Guardando hoja " + sheet.title)
            semana =None
            try:
                year = (sheet.title).split[0]
                semana = (sheet.title).split[1]
                semana = Semana.objects.get(year=year,semana=semana)
                
                
                #print("zona obtained")
            except :
                semana =None

            
            if semana == None:
                try:
                    year = (sheet.title).split[0]
                    semana = (sheet.title).split[1]
                    semana = Semana(year=year,semana=semana,creacion=str(datetime.datetime.time()))


                    semana.save(force_insert=True)
                    print("semana creada")
                    semana = Semana.objects.get(year=year,semana=semana)
                except :
                    pass
            
            
            
            

        
            letras = ['f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u']
            for i in range(0,6):

                if i != 0 and i != 1 and i != 2 and i != 4:
                    
                    print(alphabet()[i])
                    for num in range(1, sheet.max_row):
                        
                        celda = str(sheet[alphabet()[i] + str(num)].value)
                        """
                        try:
                            print("celda: " +alphabet()[i] + str(num) + " value: " + str(celda))
                        except:
                            print("celda: " +alphabet()[i] + str(num) + " value: none" )"""
                        
                        if alphabet()[i] =="A":
                            if celda != 'None':
                                if celda != "Z":
                                    if celda != "":
                                        try:
                                            zona = Zona.objects.get(codigo=int(celda))
                                            
                                            #print("zona obtained")
                                        except :
                                            zona =None

                                        
                                        if zona == None:
                                            try:
                                                zona = Zona(codigo=int(celda))

                                                zona.save(force_insert=True)
                                                #print("zona creada")
                                            except :
                                                pass
                                                #print("no anduvo")
                        if alphabet()[i] =="B":
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
                                                
                        if alphabet()[i] =="D":
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
                                                print("diagnostico creado")
                                                diagnostico = Diagnostico.objects.get(codigo=str(celda))
                                            except :
                                                #print("no anduvo crear el diagnostico")
                                                pass

                                        
                                        

                                           
                        if alphabet()[i] == "F":
                            if num != 1 and num != 2:
                                
                                try: 
                                    try:
                                        diagnostico = Diagnostico.objects.get(codigo=str(sheet["D" + str(num)].value))
                                        print("diagnostico obtained")
                                    except :
                                        print("error d")
                                        diagnostico =None
                                    try:
                                        centro = Centro.objects.get(codigo=int(str(sheet["B" + str(num)].value)))
                                        print("centro obtained")
                                    except :
                                        print("error c")
                                        centro =None
                                    
                                    
                                    for l in range(0,len(letras)):
                                        
                                        celda2 = str(sheet[letras[l] + str(num)].value)
                                        
                    
                                        if celda2 != 'None':
                                            if celda2 != ' ':
                                                try: 
                                                    cant = int(celda2)
                                                
                                                    print("se encontro una cantidad")
                                                    print("cant " + str(cant))
                                                    for h in range(0,cant):
                                                        sexo = str(sheet[letras[l] + "2"].value)
                                                        if sexo == "F":

                                                            edad = str(sheet[letras[l-1] + "1"].value).strip(" años")
                                                        else:
                                                            edad = str(sheet[letras[l] + "1"].value).strip(" años")
                                                        edad = edad.strip(" año")
                                                        
                                                        print("sexo " + sexo)
                                                        print("edad " + edad)
                                                        try: 
                                                            paciente = Paciente(sexo=sexo,edad=edad,diagnostico=diagnostico,centro=centro,semana=semana)
                                                            paciente.save(force_insert=True)
                                                            print("Paciente creado")
                                                        except :
                                                            pass
                                                            print("nos se pudo crea al paciente")
                                                except :
                                                    pass
                                                    #print("No se encontro una cantidad")
                                except:
                                    print("No se pudo obtener el centro")

       
        
        

        
        
            
        
            
            
    
    



        
    


