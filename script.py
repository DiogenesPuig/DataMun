#!/usr/bin/env python

import openpyxl
import string
from dataMun.models import *

def alphabet():
  return list(string.ascii_lowercase)


book = openpyxl.load_workbook('media/Diagnosticos_1_vez_por_CS_2021_sem_5_a_12.xlsx')

sheet = book.active
a1 = sheet['A1']
a2 = sheet['A2']
a3 = sheet.cell(row=3, column=1)

for letra in alphabet():
    num = 0
    while True:
        
        objeto = sheet[letra + str(num)]
        if objeto != None:
            if objeto != "Z":


        num += 1
    print(letra)

print(a1.value)
print(a2.value) 
print(a3.value)
