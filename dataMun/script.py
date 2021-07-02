#!/usr/bin/env python

import openpyxl
import string
from .models import *
import math
import random



def alphabet():
    return list(string.ascii_lowercase)


def read_excel(spread_sheet):
    errors = ["None"]
    print(spread_sheet.file)

    zona = 0
    cs = 0
    cname = ""
    cod = ""
    diag = ""

    workbook = openpyxl.load_workbook(spread_sheet.file)
    alphabe = alphabet()
    letras = ['f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u']
    centers = Center.objects.all()
    centers_cods = []
    for i in centers:
        centers_cods.append(i.code)

    diagnostics = Diagnostic.objects.all()
    diagnostics_cods = []
    for i in diagnostics:
        diagnostics_cods.append(i.code)

    zones = Zone.objects.all()
    zones_cods = []
    for i in zones:
        zones_cods.append(i.code)

    for sheet in workbook.worksheets:
        print("Saving week: " + sheet.title)
        crearPacientes = False

        try:
            year = (sheet.title).split(' ')[0]
            week = (sheet.title).split(' ')[1]
            week = Week.objects.get(year=int(year), week=(int(week)-5))

            crearPacientes = False
        except:
            week = None

        if week == None:
            try:
                year = (sheet.title).split(' ')[0]
                week = (sheet.title).split(' ')[1]
                week = Week(year=year, week=week, spread_sheet=spread_sheet)
                week.save()

                week = (sheet.title).split(' ')[1]
                week = Week.objects.get(year=year, week=week)
                print("week added")
                crearPacientes = True
            except:
                print("error: week dont added correctly.")
                error = [2, "(week dont added correctly.),"]
                errors.append(error)

                crearPacientes = False

            if crearPacientes:
                for row in sheet.iter_rows(values_only=True):
                    if row[4] != "Totales":
                        try:
                            zona = int(row[0])
                            cs = int(row[1])
                            cname = str(row[2])
                            cod = str(row[3])
                            diag = str(row[4])
                        except:
                            print("error obteniendo datos")
                        if zona not in zones_cods:
                            nzona = Zone(code=zona)
                            nzona.save()
                            zones_cods.append(zona)
                        if cs not in centers_cods:
                            ozona = Zone.objects.get(code=zona)
                            ncentro = Center(code=cs, name=cname, zone=ozona)
                            ncentro.save()
                            centers_cods.append(cs)
                        if cod not in diagnostics_cods:
                            ndiagnostico = Diagnostic(code=cod, name=diag)
                            ndiagnostico.save()
                            diagnostics_cods.append(cod)
                        try:
                            ocentro = Center.objects.get(code=cs)
                            odiagnostico = Diagnostic.objects.get(code=cod)
                        except:
                            print("error de centro y diagnostico")
                            ocentro = None
                            odiagnostico = None

                        if ocentro != None and odiagnostico != None:
                            for i in range(5, sheet.max_column-1):
                                sexo = ""
                                edad = 0
                                cant = 0
                                try:
                                    cant = int(row[i])
                                    if i % 2 != 0:
                                        sexo ="M"
                                        edad = str(sheet[letras[i-5] + "1"].value)
                                    else:
                                        sexo = "F"
                                        edad = str(sheet[letras[i-6] + "1"].value)

                                    edad = edad.strip(" años")
                                    edad = edad.strip(" año")

                                    try:
                                        npaciente = DiagnosticCases(sex=sexo, age=edad, cases=cant, diagnostic=odiagnostico, center=ocentro, week=week)
                                        npaciente.save()
                                    except:
                                        print("Error creando paciente")
                                except:
                                    pass

    error = [1, "(File is not a zip file.),"]
    errors.append(error)
    return errors


class DotsGraphicAverage():
    def __init__(self, average, week, lower_rank, top_rank,cases):
        self.average = average
        self.week = week
        self.lower_rank = lower_rank
        self.top_rank = top_rank
        self.cases = cases



def GetGraphicAverages(diagnostic_cases, diagnostic, weeks,year, n_years):
    curent_year = year
    weeks_current_year = weeks.filter(year=curent_year)
    weeks = weeks.filter(year__lt=year)
    
    
    #cases per diagnostic
    diagnostic_cases_w = diagnostic_cases

    #arithmetic average of the weeks / n_years
    averages = [0] * 52

    standard_deviations = [0] * 52
    #number of years
    
    #cases per week of the diferent years
    cases_per_weeks = [0] * 52
    
    for i in range(len(averages)):
        cases = 0 
        
        f = []
        year = 0
        
        suma2 = 0
        for week in weeks:
            if week.week == i+1:
                
                cases = 0
                for p in diagnostic_cases_w:
                    if p.week == week:
                        cases += p.cases
                    
                f.append(cases)

        if cases != 0:
            
            average = cases / n_years
            
            averages[i] = average
            #calculation of standar deviation
            standard_deviation = 0 
            if len(f) != 0:
                for cases in f:
                    suma2 += (cases-average)**2
                
                standard_deviation = math.sqrt(suma2 / len(f))
                standard_deviations[i] = standard_deviation
            
            
            
        
        cases = 0
        for week in weeks_current_year:
            if week.week == i+1:
                dia = diagnostic_cases.filter(week=week)
                
                for d in dia:
                    #print(d.cases)
                    
                    cases += d.cases
        cases_per_weeks[i] = cases
        
    
    #array of class dots for draw the chart of averages
    dots_graphic_averages = []
    #array of class dots for draw the chart of cumulative
    dots_graphic_cumulative = []


    average_cumulative = 0
    top_rank_cumulative = 0
    cases_acumulative = 0
    lower_rank_cumulative = 0

    for i in range(len(standard_deviations)):
        lower_rank = 0
        top_rank = 0
        cases_acumulative += cases_per_weeks[i]
        average_cumulative += averages[i]
        if n_years != 0:
            
            lower_rank = averages[i] - (4.30 * standard_deviations[i] / math.sqrt(n_years))
            top_rank = averages[i] + (4.30 * standard_deviations[i] / math.sqrt(n_years))
        if lower_rank >= 0:
            lower_rank_cumulative += lower_rank
        top_rank_cumulative += top_rank
        

        dots_average = DotsGraphicAverage(averages[i],i+1, lower_rank, top_rank,cases_per_weeks[i])
        dots_cumulative = DotsGraphicAverage(average_cumulative,i+1, lower_rank_cumulative, top_rank_cumulative,cases_acumulative)
        dots_graphic_averages.append(dots_average)
        dots_graphic_cumulative.append(dots_cumulative)
    
   


    return dots_graphic_averages, dots_graphic_cumulative


def GetAlert(diagnostic_cases, diagnostic, week,year):

    #cases per diagnostic
    
    diag_cases = diagnostic_cases.filter(diagnostic=diagnostic)
    average = 0
    standard_deviation = 0 
    cases = 0 
    #number of years
    n_years = 0
    year_var = 0
    f = []
    weeks = Week.objects.filter(year__lt=year,week=week.week).order_by('year')
    for w in weeks:

        
        if year_var != w.year:
            n_years += 1
            year_var = w.year

        
        pac = diag_cases.filter(week=w)
        x = 0
        for p in pac:
            
            cases += p.cases
            x = p.cases
            f.append(x)

    if cases != 0:
        
        average = cases / n_years

        #calculation of standar deviation  
        if len(f) != 1:
            suma2 = 0 
            for cases in f:
                suma2 += (cases-average)**2
            standard_deviation = math.sqrt(suma2 / len(f))
    cases = 0  
    dia = diag_cases.filter(week=week)
    
    for d in dia:
        #print(d.cases)
        
        cases += d.cases

    #array of class dots for draw the chart

    lower_rank = 0
    top_rank = 0
    if n_years != 0:
        lower_rank = average - (3.18 * standard_deviation / math.sqrt(n_years))
        top_rank = average + (3.18 * standard_deviation / math.sqrt(n_years))

    dots = DotsGraphicAverage(average,week.week, lower_rank, top_rank,cases)
        
    return dots


class DotsGraphicQuartile():
    def __init__(self,q1,q2,q3,cases,week):
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3
        self.cases = cases
        self.week  = week

def GetGraphicQuartiles(diagnostic_cases, diagnostic, weeks,year, n_years):
    #idk la verdad
    current_year = year
    weeks_current_year = weeks.filter(year=current_year)
    weeks = weeks.filter(year__lte=year-1)
    
    

    suma = 0
    if n_years % 2 != 0:
        suma = -1
    q = [(n_years+suma)*1 / 4,(n_years+suma)*2 / 4,(n_years+suma)*3 / 4]

    
    diagnost_cases = diagnostic_cases
    
    
    dots_graphic_quartiles = [ ]
    for o in range(52):
        dots_q=[]
        
        cases_per_years = [0.0] * (n_years)
        for i in range(len(cases_per_years)):

            cases = 0 
            
            
            for week in weeks:
                if week.week == o+1:
                    if week.year != year-(i+1):
                        cases = 0
                        for p in diagnostic_cases:
                            if p.week == week:
                                cases += p.cases

            
            if cases != 0:
                cases_per_years[i] = float(cases)
            
                
        
        n = len(  cases_per_years )
        for i in range(n-1): # range(n) also work but outer loop will repeat one time more than 
            for j in range(0, n-i-1):
                if cases_per_years[j] <  cases_per_years[j + 1] :
                    
                    l = cases_per_years[j]
                    cases_per_years[j] = cases_per_years[j + 1]
                    cases_per_years[j + 1] = l 
        
        for r in range(len(q)):
            
            dots_q.append(cases_per_years[int(q[r])])
        
        
        cases_per_week = 0 
        
        
        for week in weeks_current_year:
            if week.week == o+1 :
                dia = diagnost_cases.filter(week=week)
                
                for d in dia:
                    
                    cases_per_week += d.cases
       

        dots = DotsGraphicQuartile(dots_q[0],dots_q[0]+dots_q[1],dots_q[0]+dots_q[1]+dots_q[2],cases_per_week,o+1)
        dots_graphic_quartiles.append(dots)

    return dots_graphic_quartiles


