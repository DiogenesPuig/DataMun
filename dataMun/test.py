import openpyxl

import json
import sqlite3

workbook = openpyxl.load_workbook('Diagnosticos 1° vez por CS 2021 sem 5 a 12.xlsx')

def workbookToJson(workbook):
    rows = {}
    rows['rows'] = []
    for sheet in workbook.worksheets:
        fila = 0
        for row in sheet.iter_rows(min_row=2,values_only=True):
            existe = False
            cols = [''] * 21
            for i in range(len(cols)):
                try:
                    cols[i] = str(row[i]).rstrip()
                    if  cols[i] == "":
                        cols[i] = "null"
                    if not existe :
                        if cols[i] == "None":
                            existe = True
                        if  "=SUBTOTAL" in cols[i]:
                            existe = True
                except:
                    cols[i] = "null"
            # ----
            try:
                if row[4] != "TOTALES" and not existe:
                    rows['rows'].append({
                        'zona':cols[0],
                        'codigo_centro':cols[1],
                        'centro_name':cols[2],
                        'cod_diag':cols[3],
                        'diag':cols[4],
                        '<1M':cols[5],
                        '<1F':cols[6],
                        '1M':cols[7],
                        '1F':cols[8],
                        '2a5M':cols[9],
                        '2a5F':cols[10],
                        '6a10M':cols[11],
                        '6a10F':cols[12],
                        '11a14M':cols[13],
                        '11a14F':cols[14],
                        '15a19M':cols[15],
                        '15a19F':cols[16],
                        '20a60M':cols[17],
                        '20a60F':cols[18],
                        '61>M':cols[19],
                        '61>F':cols[20]
                    })
                    #print(rows['rows'][fila])
            except:
                pass
            fila+=1
    #print(len(rows['rows']))

    return rows

dict = workbookToJson(workbook)
print("finalizado el el workbookToJson")
conn = sqlite3.connect('../db.sqlite3')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS raw (zona INTEGER,cod_centro INTEGER, center_name VARCHAR(20), cod_diag VARCHAR(10),diag VARCHAR(50), aM INTEGER,aF INTEGER, bM INTEGER,bF INTEGER, cM INTEGER,cF INTEGER, dM INTEGER,dF INTEGER, eM INTEGER,eF INTEGER, fM INTEGER,fF INTEGER, gM INTEGER,gF INTEGER, hM INTEGER,hF INTEGER);")

command = "insert into raw values"
val = ""
i = 0
length = len(dict['rows']) -1
print(dict['rows'][0]["zona"])
for row in dict['rows']:
    
    val += "("
    l = 0
    for celda in row:
        
        if l == 2 or l== 3 or l == 4:
            val += "'" + row[celda] + "',"
        else:
            if l == 20:
                val += row[celda] 
                break
            else: 
                val += row[celda] + ","
        l += 1
     
    if i == length:
        val += ")"
        break
    else:
        val += "),"

    i += 1

val += ";"

print("finalizado el srting")
command += val
c.execute(command)
conn.commit()
conn.close()




