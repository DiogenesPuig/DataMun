#!/usr/bin/env python

import openpyxl
import string
from .models import *
import math
import random
from time import time
import sqlite3

import openpyxl
import psycopg2
from django.conf import settings

def workbookToSqlStatements(workbook,table_name,sheet_name_0,sheet_name_splitter,sheet_name_1,cols_name,ints,length_varchar,min_row):
    """
    Returns create and insert sql statement's from a given workbook 
    """
    create_sql_statement = ""
    create_sql_statement = f"CREATE TABLE IF NOT EXISTS {table_name} "
    create_sql_statement += f"(id SERIAL PRIMARY KEY , {sheet_name_0} INT, {sheet_name_1} INT,"
    cols = str(cols_name).strip("]")
    cols = cols.strip("[")
    for i in range(len(cols_name)):
        cols = cols.replace("'","")
        cols = cols.replace("'","")
        if i in ints:
            create_sql_statement += f"{cols_name[i]} INT"
        else:
            create_sql_statement += f"{cols_name[i]} CHAR({length_varchar})"
        
        if i != len(cols_name) - 1:
            create_sql_statement += ","
    create_sql_statement += ");"
    

    insert_sql_statement = ""
    insert_sql_statement = f"insert into {table_name} ({sheet_name_0},{sheet_name_1},{cols}) values "
    for sheet in workbook.worksheets:
        sheet_name_list = str(sheet.title).split(sheet_name_splitter)
        year = sheet_name_list[0]
        week = sheet_name_list[1]
        for row in sheet.iter_rows(min_row=min_row,values_only=True):
            values = "("
            values += f"{year},{week}," 
            insert = True
            for i in range(len(cols_name)):
                try:
                    if i in ints:
                        
                        cell = str(row[i])
                        try:
                            values += f"{int(cell)}"
                        except:
                            values += "null"
                    else:
                        if str(row[i]) != "" and str(row[i]) != "None":
                            values += f"'{str(row[i]).rstrip()}'"
                        else:
                            insert = False
                    
                    if i != len(cols_name) - 1:
                        values += ","
                    else:  
                        break
                except:
                    return print("error the length of the list cols_name exeed the length of max columns of the sheet")
                
            values += ")"

            if insert:
                insert_sql_statement += values + ",\n"
    temp = len(insert_sql_statement)
    insert_sql_statement = insert_sql_statement[:temp - 2]
    insert_sql_statement += ";"

    #insert_sql_statement = insert_sql_statement.replace(",\n;","\n;")
    return create_sql_statement, insert_sql_statement

hostname = settings.DATABASES["default"]["HOST"]
username = settings.DATABASES["default"]["USER"]
password = settings.DATABASES["default"]["PASSWORD"]
database = settings.DATABASES["default"]["NAME"]



def insertWorkbook(spread_sheet):
    start_total = time()
    #conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    conn = sqlite3.connect('db.sqlite3')
    print(spread_sheet.file)
    start = time()
    print("load_workbook started")
    workbook = openpyxl.load_workbook(filename=spread_sheet.file,read_only=True)
    print(f"load_workbook finished after {round(time()-start,4)} seconds")
    c = conn.cursor()
    start = time()
    print("workbookToSqlStatements started")
    create_sql_statement, insert_sql_statement = workbookToSqlStatements(workbook,"raw","year"," ","week",["col0","col1","col2","col3","col4","col5","col6","col7","col8","col9","col10","col11","col12","col13","col14","col15","col16","col17","col18","col19","col20"],[0,1,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],70,2)        
    print(f"workbookToSqlStatements finished after {round(time()-start,4)} seconds")
    #print("finalizado el srting:",insert_sql_statement)
    #print(create_sql_statement)
    start = time()
    print("create_sql_statement started")
    c.execute(create_sql_statement)
    print(f"create_sql_statement finished after {round(time()-start,4)} seconds")
    delete_table = "delete from raw;"

    start = time()
    print("delete_table started")
    c.execute(delete_table)
    print(f"delete_table finished after {round(time() - start, 4)} seconds")

    start = time()
    print("insert_sql_statement started")
    c.execute(insert_sql_statement)
    print(f"insert_sql_statement finished after {round(time()-start,4)} seconds")
    conn.commit()
    print(f"commit finished after {round(time()-start,4)} seconds")
    
    workbook.close()
    conn.close()
    print(f"total finished after {round(time()-start_total,4)} seconds")


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
                    
                    cases += d.cases  # se tiene que dividir por la poblacion_total multiplicar * 100000) y sumarle 1 ((d.cases/p_total * 100000 ) +1)
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


