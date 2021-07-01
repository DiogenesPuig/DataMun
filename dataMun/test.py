import openpyxl
import pandas as pd
import json
import sqlite3

workbook = openpyxl.load_workbook('Diagnosticos 1° vez por CS 2021 sem 5 a 12.xlsx')

def workbookToJson(workbook):
    rows = {}
    rows['rows'] = []
    for sheet in workbook.worksheets:
        fila = 0
        for row in sheet.iter_rows(min_row=2,values_only=True):
            cols = [''] * 21
            for i in range(len(cols)):
                try:
                    cols[i] = str(row[i]).rstrip()
                except:
                    cols[i]=''
            # ----
            try:
                if row[4] != "TOTALES":
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

conn = sqlite3.connect('../db.sqlite3')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS raw (zona VARCHAR(1),cod_centro )")

command = "insert into raw values (?)"
val = ""

for row in dict['rows']:
    print(json.dumps(row))
    val += "(" +json.dumps(row) + "), "


#c.execute(command,val)
#conn.commit()
#conn.close()




