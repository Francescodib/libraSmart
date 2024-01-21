from methods.crud_generic import add_utente,find_edit_utente

def submenu_utenti(Session):
    while True:
        print("\n ▪▪ Gestione Utenti ▪")
        print("1. Aggiungi Utente")
        print("2. Ricerca e modifica Utente")
        print("0. Torna al livello superiore")
        
        scelta = input("Scegli un'opzione: ")
        if scelta == "1":
            add_utente(Session)
        elif scelta == "2":
            find_edit_utente(Session)
        elif scelta == "0":
            break