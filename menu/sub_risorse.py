from methods.crud_risorse import add_risorsa,dettagli_risorsa,edit_risorsa

def submenu_risorse(Session):
    while True:
        print("\n ▪ Gestione Risorse ▪")
        print("1. Nuova Risorsa")
        print("2. Controlla dettagli e disponibilità")
        print("3. Modifica Risorsa")
        print("0. Torna al Menù Principale")

        scelta = input("Scegli un'opzione: ")
        if scelta == "1":
            add_risorsa(Session)
        elif scelta == "2":
            dettagli_risorsa(Session)
        elif scelta == "3":
            edit_risorsa(Session)
        elif scelta == "0":
            break