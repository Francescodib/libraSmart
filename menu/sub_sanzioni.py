from methods.crud_sanzioni import add_sanzione,search_and_edit_sanzioni

def submenu_sanzioni(Session):
    while True:
        print("\n ▪ Sanzioni ▪")
        print("1. Nuova Sanzione")
        print("2. Ricerca e Modifica Sanzione")
        print("0. Torna al Menù Principale")

        scelta = input("Scegli un'opzione: ")
        if scelta == "1":
            add_sanzione(Session)
        elif scelta == "2":
            search_and_edit_sanzioni(Session)
        elif scelta == "0":
            break