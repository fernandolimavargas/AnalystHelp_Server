import pyodbc

server = 'linxdmshelpdev.database.windows.net'
database = 'linxdmshelpDev'
username = 'linxdmsadmin'
password = 'ASDFqwer!@#$1234'
driver = '{ODBC Driver 17 for SQL Server}'

cnxn = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE=' +
                      database+';UID='+username+';PWD=' + password)

database_help = cnxn.cursor()
