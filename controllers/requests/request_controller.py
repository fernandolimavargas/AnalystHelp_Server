import pyodbc
import cx_Oracle
from extensions.database import database
from extensions.database_help import database_help
from models.models import MOV_SOL

def request_movements_list(user_id, user_type, request_id):
    result = []

    result_mov = database.session.query(MOV_SOL).filter(MOV_SOL.ID_SOL == request_id).all()

    for mov in result_mov:
        result.append({
            "idReq": mov.ID_SOL,
            "typeReq": mov.TIPO_SOL,
            "title": mov.TITULO,
            "type": mov.TIPO,
            "helper": mov.HELPER,
            "analyst": mov.ANALISTA,
            "resume": mov.RESUMO,
            "status": mov.STATUS,
            "dtaCreate": mov.DTA_CREATE.strftime("%d/%m/%Y %H:%M:%S")
        })

    return result

def test_connection(structure, server, database_con, username, password):
    try:
        if structure == 'SQL Server':
            driver_sqlserver = '{ODBC Driver 17 for SQL Server}'
            pyodbc.connect(f'DRIVER={driver_sqlserver};SERVER=tcp:{server};PORT=1433;DATABASE={database_con};UID={username};PWD={password}')
        
        elif structure == 'Oracle':
            cx_Oracle.connect(f'{username}/{password}@{server}/{database_con}')

        return {"message": "Conexão correta"}, 200
    except:
        return {"message": "Conexão incorreta"}, 406

def search_menu(cod_menu):
    menu = database_help.execute(f'select * from menu where cod_menu = {cod_menu}').fetchall()

    loop = True

    nome_menu = []

    while loop == True:
        nome_menu.append(menu[0][3])
        if menu[0][2] != None:
            menu = database_help.execute(f'select * from menu where cod_menu = {menu[0][2]}').fetchall()
        else:
            loop = False

    nome_menu = r" -> ".join(map(str, nome_menu[::-1])) 

    return {"message": nome_menu}