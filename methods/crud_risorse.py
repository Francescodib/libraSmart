import datetime
import models.models as mod

from methods.crud_generic import add_object_opened_session

# Funzione per selezionare o aggiungere un autore
def sel_add_autore(session):
    while True:
        autori = session.query(mod.Autore).all()
        
        print("\n Elenco Autori:")
        for i, autore in enumerate(autori):
            print(f"{i+1}. {autore.nome} {autore.cognome}")
        
        scelta = input("\n Selezionare un Autore esistente (inserisci il numero) o 0 per aggiungerne uno nuovo: ").strip()
        if scelta == "0":
            nome = input("\n Inserisci il nome del nuovo autore: ")
            cognome = input("\n Inserisci il cognome del nuovo autore: ")
            nuovo_autore = mod.Autore(nome=nome, cognome=cognome)
            add_object_opened_session(session, nuovo_autore)
            return nuovo_autore
        elif scelta.isdigit():
            scelta_autore = int(scelta)
            if 1 <= scelta_autore <= len(autori):
                return autori[scelta_autore - 1]
            else:
                print("\n Scelta non valida. Riprova.")
        else:
            print("\n Scelta non valida. Riprova.")
            
# Funzione per selezionare o aggiungere un autore
def sel_add_genere(session):
    while True:
        generi = session.query(mod.Genere).all()
        print("\n Elenco Generi:")
        for i, genere in enumerate(generi):
            print(f"{i+1}. {genere.descrizione} ")
        
        scelta = input("\n Selezionare un Genere esistente (inserisci il numero) o 0 per aggiungerne uno nuovo: ").strip()
        if scelta == "0":
            descr = input("\n Inserisci il nuovo Genere: ")
            nuovo_genere = mod.Genere(descrizione=descr)
            add_object_opened_session(session, nuovo_genere)
            return nuovo_genere
        elif scelta.isdigit():
            scelta_genere = int(scelta)
            if 1 <= scelta_genere <= len(generi):
                return generi[scelta_genere - 1]
            else:
                print("\n Scelta non valida. Riprova.")
        else:
            print("\n Scelta non valida. Riprova.")
            
# Funzione per selezionare o aggiungere un autore
def sel_add_tipo(session):
    while True:
        tipi = session.query(mod.Tipo).all()
        print("\n Elenco Tipi:")
        for i, tipo in enumerate(tipi):
            print(f"{i+1}. {tipo.descrizione} ")
        scelta = input("\n Selezionare un Tipo esistente (inserisci il numero) o 0 per aggiungerne uno nuovo: ").strip()
        if scelta == "0":
            descr = input("\n Inserisci il nuovo Tipo: ")
            nuovo_tipo = mod.Tipo(descrizione=descr)
            add_object_opened_session(session, nuovo_tipo)
            return nuovo_tipo
        elif scelta.isdigit():
            scelta_tipo = int(scelta)
            if 1 <= scelta_tipo <= len(tipi):
                return tipi[scelta_tipo - 1]
            else:
                print("\n Scelta non valida. Riprova.")
        else:
            print("\n Scelta non valida. Riprova.")

# Funzione per selezionare o aggiungere un autore
def sel_add_position(session):
    while True:
        posizioni = session.query(mod.Posizione).all()
        print("\n Elenco Posizioni:")
        for i, posizione in enumerate(posizioni):
            print(f"{i+1}. {posizione.descrizione} ")
        scelta = input("\n Selezionare Posizione esistente (inserisci il numero) o 0 per aggiungerne una nuova: ").strip()
        if scelta == "0":
            descr = input("\n Inserisci nuova Posizione: ")
            nuova_pos = mod.Posizione(descrizione=descr)
            add_object_opened_session(session, nuova_pos)
            return nuova_pos
        elif scelta.isdigit():
            scelta_pos = int(scelta)
            if 1 <= scelta_pos <= len(posizioni):
                return posizioni[scelta_pos - 1]
            else:
                print("\n Scelta non valida. Riprova.")
        else:
            print("\n Scelta non valida. Riprova.")

# Funzione per aggiungere una risorsa
def add_risorsa(Session):
    with Session() as session:
        tipo = sel_add_tipo(session)
        print (f"Tipo selezionato {tipo}")
        autore = sel_add_autore(session)
        print(f"Autore selezionato {autore}")
        genere = sel_add_genere(session)
        print(f"Genere selezionato {genere}")
        pos = sel_add_position(session)
        print(f"Posizione selezionata {pos}")
        titolo_risorsa = input("\n Inserisci Titolo Risorsa: ")
        ediz = input("\n Inserisci Edizione: ")
        anno_pub = input("\n Inserisci Anno Pubblicazione: ")
        condiz = input("\n Inserisci Condizioni: ")
        
        nuova_risorsa = mod.Risorsa(tipo=tipo,
                                    titolo=titolo_risorsa, 
                                    autore=autore, 
                                    genere=genere, 
                                    edizione=ediz, 
                                    condizioni=condiz, 
                                    anno_pubblicazione=anno_pub,
                                    posizione=pos)
        add_object_opened_session(session, nuova_risorsa)

def search_sel_risorsa(session):
    while True:
        search_id = input("\n Inserisci il codice ID della risorsa da cercare (lascia vuoto per ignorare): ").strip()
        search_title = input(" Inserisci il titolo della risorsa da cercare (lascia vuoto per ignorare): ").strip()
        search_position = input(" Inserisci la posizione della risorsa da cercare (lascia vuoto per ignorare): ").strip()

        # Effettua la ricerca delle risorse che corrispondono ai criteri
        query = session.query(mod.Risorsa).join(mod.Tipo).join(mod.Autore)

        if search_id:
            try:
                search_id = int(search_id)
                query = query.filter(mod.Risorsa.id == search_id)
            except ValueError:
                print("Codice ID non valido. Inserisci un numero intero valido.")

        if search_title:
            query = query.filter(mod.Risorsa.titolo.ilike(f"%{search_title}%"))

        if search_position:
            query = query.join(mod.Posizione).filter(mod.Posizione.descrizione.ilike(f"%{search_position}%"))

        resources_found = query.all()

        if not resources_found:
            print("Nessuna risorsa trovata.")
            return None

        # Mostra i risultati della ricerca
        print("\nRisultati della ricerca:")
        for i, resource in enumerate(resources_found):
            print(f"{i+1}. Codice ID: {resource.id}, ({resource.tipo.descrizione}) {resource.titolo} - {resource.autore.nome} {resource.autore.cognome}, Pos: {resource.posizione.descrizione}")

        scelta = input("\n Seleziona una risorsa per i dettagli (inserisci il numero) o 0 per annullare: ").strip()

        if scelta == "0":
            return None
        elif scelta.isdigit():
            scelta_risorsa = int(scelta)
            if 1 <= scelta_risorsa <= len(resources_found):
                return resources_found[scelta_risorsa - 1]

        print("Scelta non valida. Riprova.")

#method to find Risorsa and get details about Posizione and availability        
def dettagli_risorsa(Session):
    with Session() as session:
        while True:
            resource = search_sel_risorsa(session)
            if resource:
                print("\n-- Dettagli della Risorsa --")
                print(f"Codice ID: {resource.id}")
                print(f"Tipo: {resource.tipo.descrizione}")
                print(f"Titolo: {resource.titolo}")
                print(f"Autore: {resource.autore.nome} {resource.autore.cognome}")
                print(f"Edizione: {resource.edizione}")
                print(f"Condizioni: {resource.condizioni}")
                print(f"Posizione: {resource.posizione.descrizione}")

                # Verifica se la risorsa è occupata in un prestito
                prestito = session.query(mod.Prestito).filter_by(id_risorsa=resource.id, data_consegna=None).first()
                if prestito:
                    print("Stato: Occupata in un prestito")
                    data_fine_prestito = prestito.data_fine
                    oggi = datetime.date.today()
                    giorni_mancanti = (data_fine_prestito - oggi).days
                    print(f"Data di fine prestito: {data_fine_prestito.strftime('%Y-%m-%d')}")
                    print(f"Giorni mancanti alla fine del prestito: {giorni_mancanti}")

                    # Ottieni il nome, cognome e numero di telefono dell'utente che ha il prestito
                    utente_prestito = prestito.utente
                    print(f"Nome utente: {utente_prestito.nome}")
                    print(f"Cognome utente: {utente_prestito.cognome}")
                    print(f"Numero di telefono utente: {utente_prestito.telefono}")
                else:
                    print("Stato: Disponibile")

                return
            else:
                return

def edit_risorsa(Session):
    with Session() as session:
        while True:
            resource = search_sel_risorsa(session)
            if resource:
                print("\n-- Modifica della Risorsa --")
                print(f"Tipo attuale: {resource.tipo.descrizione}")
                print(f"Titolo attuale: {resource.titolo}")
                print(f"Autore attuale: {resource.autore.nome} {resource.autore.cognome}")
                print(f"Edizione attuale: {resource.edizione}")
                print(f"Condizioni attuali: {resource.condizioni}")
                print(f"Posizione attuale: {resource.posizione.descrizione}")

                # Chiedi all'utente se vuole modificare qualche campo
                scelta_modifica = input("Vuoi modificare questa risorsa? (s/n): ").strip().lower()
                if scelta_modifica != "s":
                    return

                # Modifica dei campi
                print("\n Modifica i campi interessati, lascia vuoto per non modificare valori iniziali.")
                resource.tipo = sel_add_tipo(session)
                resource.titolo = input(f"Inserisci il nuovo titolo ({resource.titolo}): ").strip() or resource.titolo
                resource.autore = sel_add_autore(session)
                resource.genere = sel_add_genere(session)
                resource.edizione = input(f"Inserisci la nuova edizione ({resource.edizione}): ").strip() or resource.edizione
                resource.condizioni = input(f"Inserisci le nuove condizioni ({resource.condizioni}): ").strip() or resource.condizioni

                # Aggiorna la posizione
                resource.posizione = sel_add_position(session)

                # Salva le modifiche
                session.commit()

                print("\n Risorsa modificata con successo.")

                return
            else:
                return