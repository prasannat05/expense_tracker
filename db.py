import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pras@2005",
        database="finance_tracker"
    )
