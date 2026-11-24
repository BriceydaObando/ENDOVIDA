

import os



def obtener_conexion():
    database_url = os.environ.get("DATABASE_URL")

    # Conexión a PostgreSQL en Neon
    if database_url:
        import psycopg
        return psycopg.connect(database_url)

    # Conexión local a SQL Server
      import pyodbc
    conexion = pyodbc.connect(
        r"DRIVER={ODBC Driver 18 for SQL Server};"
        r"SERVER=(localdb)\MSSQLLocalDB;"
        r"DATABASE=EndoVida;"
        r"Trusted_Connection=yes;"
        r"TrustServerCertificate=yes;"
    )
    return conexion


def ejecutar_consulta(cursor, consulta, parametros=None):
    # PostgreSQL utiliza %s y SQL Server utiliza ?
    if os.environ.get("DATABASE_URL"):
        consulta = consulta.replace("?", "%s")

    if parametros is None:
        cursor.execute(consulta)
    else:
        cursor.execute(consulta, parametros)
