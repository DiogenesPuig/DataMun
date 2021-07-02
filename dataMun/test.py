import openpyxl

import json
import sqlite3


def workbookToSqlStatements(workbook,table_name,sheet_name_0,sheet_name_splitter,sheet_name_1,cols_name,ints,length_varchar,min_row):
    """
    Returns create and insert sql statement's from a given workbook 
    """
    create_sql_statement = ""
    create_sql_statement = f"CREATE TABLE IF NOT EXISTS {table_name} "
    create_sql_statement += f"(id INTEGER PRIMARY KEY AUTOINCREMENT, {sheet_name_0} UNSIGNED INTEGER, {sheet_name_1} UNSIGNED INTEGER,"
    
    for i in range(len(cols_name)):
        
        if i in ints:
            create_sql_statement += f"{cols_name[i]} UNSIGNED INTEGER"
        else:
            create_sql_statement += f"{cols_name[i]} VARCHAR({length_varchar})"
        
        if i != len(cols_name) - 1:
            create_sql_statement += ","
    create_sql_statement += ");"
    cols = str(cols_name).strip("]")
    cols = cols.strip("[")
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
                        
                        cell = str(row[i]).rstrip()
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

    insert_sql_statement += ";"
    insert_sql_statement = insert_sql_statement.replace(",\n;","\n;")
    return create_sql_statement, insert_sql_statement


def insertWorkbook(workbook):
    conn = sqlite3.connect('../db.sqlite3')
    c = conn.cursor()
    create_sql_statement, insert_sql_statement = workbookToSqlStatements(workbook,"raw","year"," ","week",["col0","col1","col2","col3","col4","col5","col6","col7","col8","col9","col10","col11","col12","col13","col14","col15","col16","col17","col18","col19","col20"],[0,1,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],70,2)        
    #print("finalizado el srting:",insert_sql_statement)
    #print(create_sql_statement)
    drop_table = "drop table if exists raw;"
    c.execute(drop_table)
    c.execute(create_sql_statement)
    c.execute(insert_sql_statement)
    conn.commit()
    conn.close()




