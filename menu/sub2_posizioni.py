from methods.crud_generic import add_posizione,find_edit_posizione

def sub2_posizioni(Session):
    while True:
        print("\n ▪▪ Gestione Posizioni ▪")
        print("1. Aggiungi Posizione")
        print("2. Ricerca e modifica Posizione")
        print("0. Torna al livello superiore")
        
        scelta = input("Scegli un'opzione: ")
        if scelta == "1":
            add_posizione(Session)
        elif scelta == "2":
            find_edit_posizione(Session)
        elif scelta == "0":
            break