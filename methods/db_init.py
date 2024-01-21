import mysql.connector
from models.models import *
from methods.db_populate import *
from methods.crud_generic import conferma_operazione
from conf import db_config 


def create_database():
    try:
        conn = mysql.connector.connect(host=db_config.HOST, user=db_config.USER, password=db_config.PASSWORD)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE {db_config.DB_NAME}")
        cursor.close()
        conn.close()
        print("Database creato con successo.")
        
        need_tables = input("Desideri creare le tabelle? [1.Si 0.No] ")
        if need_tables.lower() == "1":
            if conferma_operazione():
                create_tables()
        return True
    except mysql.connector.Error as e:
        print(f"Errore nella creazione del database: {e}")
        return False

def reset_database():
    if conferma_operazione():
        Base.metadata.drop_all(db_config.db_engine)
        Base.metadata.create_all(db_config.db_engine)
        print("Database resettato con successo.")

def create_tables():
    table_list = Base.metadata.sorted_tables
    print("Tabelle che verranno create:")
    for table in table_list:
        print(table.name)
    
    if conferma_operazione():
        Base.metadata.create_all(db_config.db_engine)
        print("Tabelle create con successo.")

def seed_example_data(Session):
        reset_database()
        popola_database(Session)
        popola_tabelle_con_dipendenze(Session)