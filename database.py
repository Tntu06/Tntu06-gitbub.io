import pyodbc

def get_connection():
    return pyodbc.connect(
        "DRIVER={......};"
        "SERVER=.....;"
        "DATABASE=QUANLYBANHANG;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )


