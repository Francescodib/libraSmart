from methods.crud_generic import add_genere,find_edit_genere
def sub2_generi(Session):
    while True:
        print("\n ▪▪ Gestione Generi ▪")
        print("1. Aggiungi Genere")
        print("2. Ricerca e modifica Genere")
        print("0. Torna al livello superiore")
        
        scelta = input("Scegli un'opzione: ")
        if scelta == "1":
            add_genere(Session)
        elif scelta == "2":
            find_edit_genere(Session)
        elif scelta == "0":
            break