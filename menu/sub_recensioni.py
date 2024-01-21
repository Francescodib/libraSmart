from methods.crud_recensioni import add_recensione, search_and_edit_recensioni

def submenu_recensioni(Session):
    while True:
        print("\n ▪ Recensioni ▪")
        print("1. Nuova Recensione")
        print("2. Ricerca e Modifica Recensione")
        print("0. Torna al Menù Principale")

        scelta = input("Scegli un'opzione: ")
        if scelta == "1":
            add_recensione(Session)
        elif scelta == "2":
            search_and_edit_recensioni(Session)
        elif scelta == "0":
            break