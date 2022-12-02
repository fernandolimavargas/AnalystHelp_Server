from urllib import parse
from flask_sqlalchemy import SQLAlchemy


def init_app(app):
    parametros = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=linxdmshelpdev.database.windows.net;"
        "PORT=1433;"
        "DATABASE=linxdmshelpDev;"
        "UID=linxdmsadmin;"
        "PWD=ASDFqwer!@#$1234"
    )

    url_db = parse.quote_plus(parametros)

    app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc:///?odbc_connect={url_db}"
    app.config['SQLALCHEMY_POOL_SIZE'] = 200
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    SQLAlchemy(app)


database = SQLAlchemy()
