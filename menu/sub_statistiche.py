from methods.crud_statistiche import stat_call

def submenu_statistiche(Session):
    while True:
        print("\n ▪ Statistiche ▪")
        print("1. Mostra 10 Risorse più richieste")
        print("2. Mostra 10 Risorse più votate")
        print("3. Mostra 10 Utenti con più sanzioni")
        print("0. Torna al Menù Principale")

        scelta = input("Scegli un'opzione: ")
        if scelta == "1":
            stat_call(Session,"ris_richieste")
        elif scelta == "2":
            stat_call(Session,"ris_voto")
        elif scelta == "3":
            stat_call(Session,"ute_sanzioni")
        elif scelta == "0":
            break