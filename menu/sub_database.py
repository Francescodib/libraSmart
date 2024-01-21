from methods import db_init

def submenu_database(Session):
    while True:
        print("\n ▪ Gestione Database ▪")
        print("1. Crea Database")
        print("2. Resetta Database")
        print("3. Crea Tabelle")
        print("4. Popola Tabelle con dati test")
        print("0. Torna al Menù Principale")

        scelta = input("Scegli un'opzione: ")
        if scelta == "1":
            db_init.create_database()
        elif scelta == "2":
            db_init.reset_database()
        elif scelta == "3":
            db_init.create_tables()
        elif scelta == "4":
            db_init.seed_example_data(Session)
        elif scelta == "0":
            break