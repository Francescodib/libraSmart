from methods.crud_prestiti import add_prestito,search_edit_prestito,list_close_prestito,add_prenotazione, search_prenotazioni

def submenu_prestiti(Session):
    while True:
        print("\n ▪ Prestiti & Prenotazioni ▪")
        print("1. Nuovo Prestito")
        print("2. Ricerca e Modifica Prestito")
        print("3. Registra chiusura Prestito")
        print("4. Nuova Prenotazione")
        print("5. Ricerca e modifica Prenotazione")
        print("0. Torna al Menù Principale")

        scelta = input("Scegli un'opzione: ")
        if scelta == "1":
            add_prestito(Session)
        elif scelta == "2":
            search_edit_prestito(Session)
        elif scelta == "3":
            list_close_prestito(Session)
        elif scelta == "4":
            add_prenotazione(Session)
        elif scelta == "5":
            search_prenotazioni(Session)
        elif scelta == "0":
            break
