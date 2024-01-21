from menu import sub2_tipi,sub2_generi,sub2_posizioni

def submenu_prop_risorse(Session):
    while True:
        print("\n ▪ Proprietà risorse ▪")
        print("1. Tipi")
        print("2. Generi")
        print("3. Posizioni")
        print("0. Torna al Menù Principale")

        scelta = input("Scegli un'opzione: ")
        if scelta == "1":
            sub2_tipi.sub2_tipi(Session)
        elif scelta == "2":
            sub2_generi.sub2_generi(Session)
        elif scelta == "3":
            sub2_posizioni.sub2_posizioni(Session)
        elif scelta == "0":
            break