import pyodbc

server = 'linxkpis.database.windows.net'
database = 'kpisprd'
username = '{svc_kpis_tools_ro_automotivo@linx.com.br}'
password = '{n$8aL^dgTz5p}'
driver = '{ODBC Driver 17 for SQL Server}'
authentication = 'ActiveDirectoryPassword'


cnxn = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE=' +
                      database+';UID='+username+';PWD=' + password + ';Authentication=' + authentication)

database_azure = cnxn.cursor()
