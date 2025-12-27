import pyodbc

def get_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=LAPTOP-RIA3KGI9;"
        "DATABASE=QUANLYBANHANG;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )
