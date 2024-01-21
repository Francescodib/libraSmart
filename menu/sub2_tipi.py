from methods.crud_generic import add_tipo,find_edit_tipo

def sub2_tipi(Session):
    while True:
        print("\n ▪▪ Gestione Tipi ▪")
        print("1. Aggiungi Tipo")
        print("2. Ricerca e modifica Tipo")
        print("0. Torna al livello superiore")
        
        scelta = input("Scegli un'opzione: ")
        if scelta == "1":
            add_tipo(Session)
        elif scelta == "2":
            find_edit_tipo(Session)
        elif scelta == "0":
            break