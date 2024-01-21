from menu import sub_database,prop_risorse,sub_risorse,sub_prestiti,sub_recensioni,sub_sanzioni,sub_statistiche,sub_utenti
#main menu
def main_menu(Session):
    while True:
        print("\n ▌█▚ LibraSm@rt ▞█▐ v1.0")
        print("\n ▪ Menù Principale ▪")
        print("1. Utility Database")
        print("2. Proprietà Risorse (Tipi, Generi, Posizioni)")
        print("3. Risorse")
        print("4. Utenti")
        print("5. Prestiti e Prenotazioni")
        print("6. Recensioni")
        print("7. Sanzioni")
        print("8. Statistiche")
        print("0. Esci")

        scelta = input("Scegli un'opzione: ")
        if scelta == "1":
            sub_database.submenu_database(Session)
        elif scelta == "2":
            prop_risorse.submenu_prop_risorse(Session)
        elif scelta == "3":
            sub_risorse.submenu_risorse(Session)
        elif scelta == "4":
            sub_utenti.submenu_utenti(Session)
        elif scelta == "5":
            sub_prestiti.submenu_prestiti(Session)
        elif scelta == "6":
            sub_recensioni.submenu_recensioni(Session)
        elif scelta == "7":
            sub_sanzioni.submenu_sanzioni(Session)
        elif scelta == "8":
            sub_statistiche.submenu_statistiche(Session)
        elif scelta == "0":
            break
        
    