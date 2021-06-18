#!/usr/bin/env python

import openpyxl
import string
from .models import *
import math



def alphabet():
    return list(string.ascii_lowercase)


def read_excel(spread_sheet):
    errors = ["None"]
    print(spread_sheet.file)

    

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
            week = Week.objects.get(year=year, week=week)

            crearPacientes = False
            # print("zone obtained")
        except:
            week = None

        if week == None:
            try:
                year = (sheet.title).split(' ')[0]
                week = (sheet.title).split(' ')[1]
                week = Week(year=year, week=week,spread_sheet=spread_sheet)

                week.save(force_insert=True)
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

            for i in range(0, 6):
                if i != 2 and i != 4:
                    print(alphabe[i])
                    for num in range(1, sheet.max_row):
                        if num != 1 and num != 2:
                            cell = str(sheet[alphabe[i] + str(num)].value)

                            if i == 0:
                                try:
                                    code = int(cell)
                                except:
                                    pass
                                if code not in zones_cods:
                                    try:
                                        zone = Zone(code=int(cell))

                                        zone.save(force_insert=True)
                                        zones_cods.append(int(cell))
                                        # print("zone added")
                                    except:
                                        pass

                            elif i == 1:
                                try:
                                    code = int(cell)
                                except:
                                    pass
                                if code not in centers_cods:
                                    try:
                                        zone = Zone.objects.get(code=int(str(sheet["A" + str(num)].value)))
                                        center = Center(code=int(cell), name=str(sheet["C" + str(num)].value),zone=zone)
                                        center.save(force_insert=True)
                                        centers_cods.append(int(cell))
                                        # print("Center creado")
                                    except:
                                        pass

                            elif i == 3:
                                try:
                                    code = str(cell)
                                except:
                                    pass
                                if code not in diagnostics_cods and code != 'None':
                                    try:
                                        diagnostic = Diagnostic(code=str(cell),name=str(sheet["E" + str(num)].value))
                                        diagnostic.save(force_insert=True)
                                        diagnostics_cods.append(str(cell))
                                        # print("Diagnostic creado")
                                    except:
                                        pass

                            elif i == 5:
                                if str(sheet["E" + str(num)].value) != "TOTALES":
                                    try:
                                        diagnostic = Diagnostic.objects.get(code=str(sheet["D" + str(num)].value))
                                        # print("Diagnostic obtained")
                                    except:
                                        print("error d")
                                        diagnostic = None
                                    try:
                                        center = Center.objects.get(code=int(str(sheet["B" + str(num)].value)))
                                        # print("Center obtained")
                                    except:
                                        print("error c")
                                        center = None

                                    if center != None and diagnostic != None:
                                        for l in range(0, len(letras)):
                                            cell2 = str(sheet[letras[l] + str(num)].value)
                                            try:
                                                cases = int(cell2)
                                                sex = ""
                                                age = ""
                                                if (l + 1) % 2 != 0:
                                                    sex = "M"
                                                    age = str(sheet[letras[l] + "1"].value)
                                                else:
                                                    age = str(sheet[letras[l - 1] + "1"].value)
                                                    sex = "F"
                                                age = age.strip(" años")
                                                age = age.strip(" año")
                                                #cases = random.randint(1, cases*2)
                                                try:
                                                    diagnosticCases = DiagnosticCases(sex=sex, age=age,
                                                                        diagnostic=diagnostic, center=center,
                                                                        week=week,cases=cases)
                                                    diagnosticCases.save(force_insert=True)
                                                    # print("diagnosticCases creado")
                                                except:
                                                    pass
                                            except:
                                                pass
                                                # print("No se encontro una casesidad")
                                            
    #except:
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



def GetGraphicAverages(diagnostic_cases, diagnostic, weeks,year):
    
    
    weeks = weeks.filter(year__lt=year)
    curent_year = year
    #cases per diagnostic
    
    diagnostic_cases = diagnostic_cases.filter(diagnostic=diagnostic)

    #arithmetic average of the weeks / n_years
    averages = [0] * 52

    standard_deviations = [0] * 52
    #number of years
    n_years = 0
    #cases per week of the diferent years
    cases_per_weeks = [0] * 52
    
    for i in range(len(averages)):
        cases = 0 
        
        f = []
        year = 0
        n_years = 0
        suma2 = 0
        for week in weeks:
            if week.week == i+1:
                pac = diagnostic_cases.filter(week=week)
                cases
                for p in pac:
                    
                    cases += p.cases
                    
                f.append(cases)
                
            if week.year != year:
                n_years += 1
                year = week.year
        
            

            
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
            
            
                
                
                
            
        weeks_qs = Week.objects.filter(week=(i+1),year=curent_year)
        cases = 0
        for week in weeks_qs:
            
            dia = diagnostic_cases.filter(week=week)
            
            for d in dia:
                #print(d.cases)
                
                cases += d.cases
        cases_per_weeks[i] = cases
    
    #array of class dots for draw the chart
    dots_graphic_averages = []
    for i in range(len(standard_deviations)):
        lower_rank = 0
        top_rank = 0
        if n_years != 0:
            lower_rank = averages[i] - (3.18 * standard_deviations[i] / math.sqrt(n_years))
            top_rank = averages[i] + (3.18 * standard_deviations[i] / math.sqrt(n_years))
        

        dots = DotsGraphicAverage(averages[i],i+1, lower_rank, top_rank,cases_per_weeks[i])
        dots_graphic_averages.append(dots)
    
   


    return dots_graphic_averages


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
    weeks = weeks.filter(year__lte=year-1)
    current_year = year
    

    suma = 0
    if n_years % 2 != 0:
        suma = -1
    q = [(n_years+suma)*1 / 4,(n_years+suma)*2 / 4,(n_years+suma)*3 / 4]

    
    diagnost_cases = diagnostic_cases.filter(diagnostic=diagnostic)
    
    dots_graphic_quartiles = [ ]
    for o in range(52):
        dots_q=[]
        
        cases_per_years = [0.0] * (n_years)
        for i in range(len(cases_per_years)):

            cases = 0 
            
            weeks_qs = weeks.filter(year=year-(i+1),week=o+1)
            for week in weeks_qs:
                

                dia = diagnostic_cases.filter(week=week)
                
                for d in dia:
                    cases += d.cases

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
        
        weeks_qs = Week.objects.filter(week=(o+1),year=current_year)
        for week in weeks_qs:
            
            dia = diagnost_cases.filter(week=week)
            
            for d in dia:
                
                cases_per_week += d.cases
       
        
        dots = DotsGraphicQuartile(dots_q[0],dots_q[1],dots_q[2],cases_per_week,o+1)
        dots_graphic_quartiles.append(dots)

    return dots_graphic_quartiles


def GetGraphicCumulative(diagnostic_cases, diagnostic, weeks, year):
    weeks = weeks.filter(year__lt=year)
    curent_year = year
    # cases per diagnostic

    diagnostic_cases = diagnostic_cases.filter(diagnostic=diagnostic)

    # arithmetic average of the weeks / n_years
    averages = [0] * 52

    standard_deviations = [0] * 52
    # number of years
    n_years = 0
    # cases per week of the diferent years
    cases_per_weeks = [0] * 52

    for i in range(len(averages)):
        cases = 0

        f = []
        year = 0
        n_years = 0
        suma2 = 0
        for week in weeks:
            if week.week == i + 1:
                pac = diagnostic_cases.filter(week=week)
                cases
                for p in pac:
                    cases += p.cases

                f.append(cases)

            if week.year != year:
                n_years += 1
                year = week.year

        if cases != 0:

            average = cases / n_years

            averages[i] = average
            # calculation of standar deviation
            standard_deviation = 0
            if len(f) != 0:
                for cases in f:
                    suma2 += (cases - average) ** 2

                standard_deviation = math.sqrt(suma2 / len(f))
                standard_deviations[i] = standard_deviation

        weeks_qs = Week.objects.filter(week=(i + 1), year=curent_year)
        cases = 0
        for week in weeks_qs:

            dia = diagnostic_cases.filter(week=week)
            for d in dia:
                # print(d.cases)
                cases += d.cases

        cases_per_weeks[i] = cases

    # array of class dots for draw the chart
    dots_graphic_cumulative = []
    lower_rank = 0
    top_rank = 0
    cases = 0
    average = 0
    for i in range(len(standard_deviations)):
        cases += cases_per_weeks[i]
        average += averages[i]
        if n_years != 0:
            lower_rank += averages[i] - (3.18 * standard_deviations[i] / math.sqrt(n_years))
            top_rank += averages[i] + (3.18 * standard_deviations[i] / math.sqrt(n_years))

        dots = DotsGraphicAverage(average, i + 1, lower_rank, top_rank, cases)
        dots_graphic_cumulative.append(dots)

    return dots_graphic_cumulative