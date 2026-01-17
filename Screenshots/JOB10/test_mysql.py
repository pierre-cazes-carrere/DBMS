import mysql.connector
from mysql.connector import Error

try:
    conn = mysql.connector.connect(
        host="localhost",      # ou "127.0.0.1"
        user="root",
        password="",
        database="CarbonFootprint"
    )
    print("Connexion OK")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Country;")
    print("Lignes dans Country :", cursor.fetchone()[0])
    conn.close()
except Error as e:
    print("Code erreur :", e.errno)
    print("Message    :", e.msg)
