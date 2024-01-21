from models.models import Prestito, Risorsa, Utente, Prenotazione, Sanzione
from methods.crud_generic import add_object_opened_session
from sqlalchemy.orm import joinedload
import datetime

#search and select Risorsa passing an opened session
def search_select_risorsa(session):
    while True:
        tipo_risorsa = input("\n Inserisci il tipo di risorsa da cercare (lascia vuoto per ignorare): ").strip()
        titolo_risorsa = input("\n Inserisci il titolo di risorsa da cercare (lascia vuoto per ignorare): ").strip()
        autore_risorsa = input("\n Inserisci l'autore di risorsa da cercare (lascia vuoto per ignorare): ").strip()

        # Effettua la ricerca delle risorse che corrispondono ai criteri
        query = session.query(Risorsa)

        if tipo_risorsa:
            query = query.filter(Risorsa.tipo.descrizione.ilike(f"%{tipo_risorsa}%"))
        if titolo_risorsa:
            query = query.filter(Risorsa.titolo.ilike(f"%{titolo_risorsa}%"))
        if autore_risorsa:
            query = query.filter(Risorsa.autore.ilike(f"%{autore_risorsa}%"))

        risorse_trovate = query.all()

        if not risorse_trovate:
            print("Nessun risultato trovato.")
            return None

        # Mostra i risultati della ricerca
        print("\nRisultato della ricerca per Risorse disponibili al prestito:")
        for i, risorsa in enumerate(risorse_trovate):
            available = check_disponibilita_risorsa(session, risorsa.id)
            if not available:
                continue
            print(f"{i+1}. ({risorsa.tipo.descrizione}), Titolo: {risorsa.titolo}, Autore: {risorsa.autore.nome} {risorsa.autore.cognome}, {risorsa.edizione}")
        scelta = input("\n Seleziona una risorsa (inserisci il numero) o 0 per annullare: ").strip()

        if scelta == "0":
            return None
        elif scelta.isdigit():
            scelta_risorsa = int(scelta)
            if 1 <= scelta_risorsa <= len(risorse_trovate):
                return risorse_trovate[scelta_risorsa - 1]

        print("Scelta non valida. Riprova.")

#search and select Utente passing an opened session
def search_select_utente(session):
    while True:
        nome_utente = input("\n Inserisci il nome dell'utente da cercare (lascia vuoto per ignorare): ").strip()
        cognome_utente = input("\n Inserisci il cognome dell'utente da cercare (lascia vuoto per ignorare): ").strip()

        # Effettua la ricerca degli utenti che corrispondono ai criteri
        query = session.query(Utente)

        if nome_utente:
            query = query.filter(Utente.nome.ilike(f"%{nome_utente}%"))
        if cognome_utente:
            query = query.filter(Utente.cognome.ilike(f"%{cognome_utente}%"))

        utenti_trovati = query.all()

        if not utenti_trovati:
            print("Nessun utente trovato.")
            return None

        # Mostra i risultati della ricerca
        print("\nRisultati della ricerca:")
        for i, utente in enumerate(utenti_trovati):
            print(f"{i+1}. Nome: {utente.nome} {utente.cognome}, codice_id: {utente.id}")

        scelta = input("\n Seleziona un utente (inserisci il numero) o 0 per annullare: ").strip()

        if scelta == "0":
            return None
        elif scelta.isdigit():
            scelta_utente = int(scelta)
            if 1 <= scelta_utente <= len(utenti_trovati):
                return utenti_trovati[scelta_utente - 1]

        print("Scelta non valida. Riprova.")

def search_edit_prestito(Session):
    with Session() as session:
        while True:
            prestito = search_select_prestito(session)
            if prestito:
                print("\n-- Modifica del Prestito --")
                print(f"Data di inizio attuale: {prestito.data_inizio.strftime('%Y-%m-%d')}")
                print(f"Data di fine attuale: {prestito.data_fine.strftime('%Y-%m-%d')}")
                print(f"Data di consegna attuale: {prestito.data_consegna.strftime('%Y-%m-%d') if prestito.data_consegna else 'Non consegnata'}")
                print(f"Risorsa: {prestito.risorsa.titolo}")
                print(f"Utente: {prestito.utente.nome} {prestito.utente.cognome}")

                # Chiedi all'utente se vuole modificare qualche campo
                scelta_modifica = input("Vuoi modificare questo prestito? (s/n): ").strip().lower()
                if scelta_modifica != "s":
                    return

                # Modifica delle date di inizio e fine
                nuova_data_inizio = input(f"Inserisci la nuova data di inizio ({prestito.data_inizio.strftime('%Y-%m-%d')}): ").strip() or prestito.data_inizio.strftime('%Y-%m-%d')
                nuova_data_fine = input(f"Inserisci la nuova data di fine ({prestito.data_fine.strftime('%Y-%m-%d')}): ").strip() or prestito.data_fine.strftime('%Y-%m-%d')

                # Verifica che la nuova data di fine sia successiva a quella di inizio
                try:
                    nuova_data_inizio = datetime.datetime.strptime(nuova_data_inizio, '%Y-%m-%d').date()
                    nuova_data_fine = datetime.datetime.strptime(nuova_data_fine, '%Y-%m-%d').date()
                    if nuova_data_fine <= nuova_data_inizio:
                        print("La data di fine deve essere successiva a quella di inizio. Riprova.")
                        continue
                except ValueError:
                    print("Formato data non valido. Utilizza il formato 'YYYY-MM-DD'. Riprova.")
                    continue

                prestito.data_inizio = nuova_data_inizio
                prestito.data_fine = nuova_data_fine

                # Modifica della data di consegna (se il prestito è già stato consegnato)
                if prestito.data_consegna:
                    nuova_data_consegna = input(f"Inserisci la nuova data di consegna ({prestito.data_consegna.strftime('%Y-%m-%d')}): ").strip() or prestito.data_consegna.strftime('%Y-%m-%d')
                    try:
                        nuova_data_consegna = datetime.datetime.strptime(nuova_data_consegna, '%Y-%m-%d').date()
                        prestito.data_consegna = nuova_data_consegna
                    except ValueError:
                        print("Formato data non valido. Utilizza il formato 'YYYY-MM-DD'. La data di consegna rimarrà invariata.")

                # Salva le modifiche
                session.commit()

                print("Prestito modificato con successo.")

                return
            else:
                return
    
def search_select_prestito(session):
    while True:
        search_id = input("\n Inserisci il codice ID del prestito da cercare (lascia vuoto per ignorare): ").strip()
        search_id_risorsa = input("\n Inserisci il codice ID della risorsa associata al prestito da cercare (lascia vuoto per ignorare): ").strip()
        search_id_utente = input("\n Inserisci il codice ID dell'utente associato al prestito da cercare (lascia vuoto per ignorare): ").strip()

        # Effettua la ricerca dei prestiti che corrispondono ai criteri
        query = session.query(Prestito)

        if search_id:
            try:
                search_id = int(search_id)
                query = query.filter(Prestito.id == search_id)
            except ValueError:
                print("Codice ID del prestito non valido. Inserisci un numero intero valido.")

        if search_id_risorsa:
            try:
                search_id_risorsa = int(search_id_risorsa)
                query = query.filter(Prestito.id_risorsa == search_id_risorsa)
            except ValueError:
                print("Codice ID della risorsa non valido. Inserisci un numero intero valido.")

        if search_id_utente:
            try:
                search_id_utente = int(search_id_utente)
                query = query.filter(Prestito.id_utente == search_id_utente)
            except ValueError:
                print("Codice ID dell'utente non valido. Inserisci un numero intero valido.")

        prestiti_trovati = query.all()

        if not prestiti_trovati:
            print("Nessun prestito trovato.")
            return None

        # Mostra i risultati della ricerca
        print("\n Risultati della ricerca Prestito:")
        for i, prestito in enumerate(prestiti_trovati):
            print(f"{i+1}. Cod_ID: {prestito.id}, {prestito.risorsa.tipo.descrizione} {prestito.risorsa.titolo}, Utente: {prestito.utente.nome} {prestito.utente.cognome}")

        scelta = input("\n Seleziona un prestito (inserisci il numero) o 0 per annullare: ").strip()

        if scelta == "0":
            return None
        elif scelta.isdigit():
            scelta_prestito = int(scelta)
            if 1 <= scelta_prestito <= len(prestiti_trovati):
                return prestiti_trovati[scelta_prestito - 1]

        print("Scelta non valida. Riprova.")
        
def list_close_prestito(Session):
    with Session() as session:
        prestiti_aperti = search_pending_prestito(session)

        if not prestiti_aperti:
            print("Nessun prestito aperto trovato.")
            return None

        # Mostra i prestiti aperti e permette di chiuderne uno
        print("Elenco Prestiti aperti:")
        for i, prestito in enumerate(prestiti_aperti):
            print(f"\n{i+1}. Prestito cod.ID: {prestito.id} ")
            print(f"   {prestito.risorsa.tipo.descrizione} - {prestito.risorsa.titolo} - {prestito.risorsa.autore.nome} {prestito.risorsa.autore.cognome} - {prestito.risorsa.edizione}")
            print(f"   Data rientro Prevista: {prestito.data_fine}")
            # Calcola la data corrente
            oggi = datetime.date.today()

            # Verifica se il prestito è in ritardo
            if prestito.data_fine < oggi:
                print(">> Stato: In ritardo")
            else:
                print("   Stato: In corso")
                
            print(f"   Nome e Cognome utente: {prestito.utente.nome} {prestito.utente.cognome}")
            print(f"   Numero di telefono utente: {prestito.utente.telefono}")

        scelta = input("Seleziona un prestito da chiudere (inserisci il numero) o 0 per annullare: ").strip()

        if scelta == "0":
            return

        if scelta.isdigit():
            scelta_prestito = int(scelta)
            if 1 <= scelta_prestito <= len(prestiti_aperti):
                prestito_da_chiudere = prestiti_aperti[scelta_prestito - 1]
                data_consegna = input("Inserisci la data di consegna (YYYY-MM-DD, o lasciare vuoto per data odierna): ").strip()
                if not data_consegna:
                    data_consegna = datetime.date.today()
                else:
                    try:  
                        data_consegna = datetime.datetime.strptime(data_consegna, "%Y-%m-%d").date()
                    except ValueError:
                        print("Data non valida. Inserisci una data nel formato corretto (YYYY-MM-DD).")
                        return
                
                print(f"Sto registrando Prestito cod_ID: {prestito_da_chiudere.id} con la seguente data consegna {data_consegna}")    
                prestito_da_chiudere.data_consegna = data_consegna
                session.commit()
                print("Prestito chiuso e registrato correttamente.")
                sanzionare = input("Si intende procedere con la registrazione di una sanzione? s/n (lasciare vuoto per annullare):").strip().lower()
                if sanzionare != "s":
                    return
                add_sanzione_byclosing(Session,prestito_da_chiudere)

def search_pending_prestito(session):
    # Effettua la ricerca dei prestiti aperti
    query = session.query(Prestito).filter(Prestito.data_consegna == None)

    # Precarica gli attributi correlati
    query = query.options(
        joinedload(Prestito.risorsa, innerjoin=True).joinedload(Risorsa.tipo),
        joinedload(Prestito.risorsa, innerjoin=True).joinedload(Risorsa.autore),
        joinedload(Prestito.utente)
    )

    prestiti_aperti = query.all()
    return prestiti_aperti

def add_sanzione_byclosing(Session,prestito):
    with Session() as session:
        # Selezione del prestito a cui si riferisce la sanzione
        prestito_selezionato = prestito

        if not prestito_selezionato:
            print("Nessun prestito chiuso trovato o scelta annullata.")
            return

        # Chiedi all'utente di inserire l'importo e la descrizione della sanzione
        importo = input("Inserisci l'importo della sanzione: ").strip()
        descrizione = input("Inserisci una descrizione della sanzione: ").strip()

        # Creazione dell'oggetto Sanzione
        nuova_sanzione = Sanzione(
            importo=importo,
            descrizione=descrizione,
            id_prestito=prestito_selezionato.id
        )

        # Aggiunta della sanzione al database
        add_object_opened_session(session, nuova_sanzione)
    
def add_prenotazione(Session):
    with Session() as session:
        data_prenotazione = input("Inserisci la data di Prenotazione (YYYY-MM-DD, o lasciare vuoto per data odierna): ").strip()
        if not data_prenotazione:
            data_prenotazione = datetime.date.today()
        else:
            try:  
                data_prenotazione = datetime.datetime.strptime(data_prenotazione, "%Y-%m-%d").date()
            except ValueError:
                print("Data non valida. Inserisci una data nel formato corretto (YYYY-MM-DD).")
                return
        stato = "In attesa"

        risorsa = search_select_risorsa(session)
        utente = search_select_utente(session)

        nuova_prenotazione = Prenotazione(data=data_prenotazione, stato=stato, id_risorsa=risorsa.id, id_utente=utente.id)

        add_object_opened_session(session, nuova_prenotazione)

        print(f"Prenotazione registrata con successo, utente: {utente.nome} {utente.cognome}, Risorsa: {risorsa.tipo.descrizione} {risorsa.titolo} {risorsa.edizione}")
        

def search_pending_prenotazioni(session):
    # Effettua la ricerca delle prenotazioni in attesa
    query = session.query(Prenotazione).filter(Prenotazione.stato == "In attesa")

    # Precarica gli attributi correlati per ottenere informazioni sulla risorsa e sull'utente
    query = query.options(
        joinedload(Prenotazione.risorsa, innerjoin=True).joinedload(Risorsa.tipo),
        joinedload(Prenotazione.risorsa, innerjoin=True).joinedload(Risorsa.autore),
        joinedload(Prenotazione.utente)
    )

    prenotazioni_in_attesa = query.all()

    if not prenotazioni_in_attesa:
        print("Nessuna prenotazione in attesa trovata.")
        return None

    # Mostra i risultati della ricerca
    print("Prenotazioni in attesa:")
    for i, prenotazione in enumerate(prenotazioni_in_attesa):
        print(f"\n{i+1}. Data: {prenotazione.data}")
        print(f"   Risorsa: {prenotazione.risorsa.tipo.descrizione} - {prenotazione.risorsa.titolo} - {prenotazione.risorsa.autore.nome} {prenotazione.risorsa.autore.cognome} - {prenotazione.risorsa.edizione}")
        print(f"   Utente: {prenotazione.utente.nome} {prenotazione.utente.cognome}")

    return prenotazioni_in_attesa

def search_prenotazioni(Session):
    with Session() as session:
        titolo_risorsa = input("\n Ricerca Prenotazione tramite titolo Risorsa (lascia vuoto per ignorare): ").strip()
        nome_utente = input(" Ricerca Prenotazione tramite Nome Utente (lascia vuoto per ignorare): ").strip()
        cognome_utente = input(" Ricerca Prenotazione tramite Cognome Utente (lascia vuoto per ignorare): ").strip()
        filtro_aperte = input(" Vuoi mostrare solo prenotazioni 'In Attesa'? s/n (lascia vuoto per ignorare): ").strip().lower()

        # Effettua la ricerca delle prenotazioni
        query = session.query(Prenotazione)

        # Unisci le tabelle correlate per ottenere le informazioni sulla risorsa e sull'utente
        query = query.join(Risorsa, Risorsa.id == Prenotazione.id_risorsa).join(Utente, Utente.id == Prenotazione.id_utente)

        # Applica i filtri se sono stati specificati
        if titolo_risorsa:
            query = query.filter(Risorsa.titolo.ilike(f"%{titolo_risorsa}%"))
        if nome_utente:
            query = query.filter(Utente.nome.ilike(f"%{nome_utente}%"))
        if cognome_utente:
            query = query.filter(Utente.cognome.ilike(f"%{cognome_utente}%"))
        if filtro_aperte == "s":
            query = query.filter(Prenotazione.stato.ilike(f"%In attesa%"))

        prenotazioni_trovate = query.all()

        if not prenotazioni_trovate:
            print("Nessuna prenotazione trovata.")
            return None

        # Mostra i risultati della ricerca
        print("Risultati della ricerca Prenotazioni:")
        for i, prenotazione in enumerate(prenotazioni_trovate):
            print(f"\n{i+1}. Data: {prenotazione.data} - Stato: {prenotazione.stato}")
            risorsa_associata = session.query(Risorsa).get(prenotazione.id_risorsa)
            print(f"   Risorsa: {risorsa_associata.tipo.descrizione} - {risorsa_associata.titolo} - {risorsa_associata.autore.nome} {risorsa_associata.autore.cognome} - {risorsa_associata.edizione}")
            utente_associato = session.query(Utente).get(prenotazione.id_utente)
            print(f"   Utente: {utente_associato.nome} {utente_associato.cognome}")

        scelta = input("\nSeleziona una prenotazione da modificare (inserisci il numero) o 0 per annullare: ").strip()

        if scelta == "0":
            return None
        elif scelta.isdigit():
            scelta_prenotazione = int(scelta)
            if 1 <= scelta_prenotazione <= len(prenotazioni_trovate):
                prenotazione_da_modificare = prenotazioni_trovate[scelta_prenotazione - 1]
                edit_prenotazione(session, prenotazione_da_modificare)
                
def edit_prenotazione(session,prenotazione):
    nuova_data = input(f"Inserisci la nuova data per la prenotazione ({prenotazione.data.strftime('%Y-%m-%d')}): ").strip() or prenotazione.data.strftime('%Y-%m-%d')
    try:
        nuova_data = datetime.datetime.strptime(nuova_data, '%Y-%m-%d').date()
    except ValueError:
        print("Formato data non valido. Utilizza il formato 'YYYY-MM-DD'. Riprova.")
        return
    prenotazione.data = nuova_data
    nuovo_stato = input(f"Inserisci nuovo Stato per la prenotazione ({prenotazione.stato}): ").strip() or prenotazione.stato
    prenotazione.stato = nuovo_stato
    session.commit()
    print(f"Modifica Prenotazione completata correttamente")

def list_prenotazioni_pending(Session):
    with Session() as session:
        pending_prenotazioni = search_pending_prenotazioni(session)
        if not pending_prenotazioni:
            print("Nessuna prenotazione in attesa trovata.")
        else:
            print("Elenco delle prenotazioni in attesa:")
            for i, prenotazione in enumerate(pending_prenotazioni):
                risorsa = prenotazione.risorsa
                utente = prenotazione.utente
                tipo_risorsa = risorsa.tipo.descrizione
                autore_risorsa = f"{risorsa.autore.nome} {risorsa.autore.cognome}"

                print(f"{i+1}. Data: {prenotazione.data}, Stato: {prenotazione.stato}")
                print(f"   Titolo Risorsa: {risorsa.titolo}")
                print(f"   Tipo Risorsa: {tipo_risorsa}")
                print(f"   Autore Risorsa: {autore_risorsa}")
                print(f"   Nome Utente: {utente.nome}")
                print(f"   Cognome Utente: {utente.cognome}")

def add_prestito(Session):
    with Session() as session:
        # Selezione della risorsa
        risorsa_selezionata = search_select_risorsa(session)
        if(risorsa_selezionata == None):
            return
        print(f"\n Risorsa selezionata {risorsa_selezionata.id}")

        # Selezione dell'utente
        utente_selezionato = search_select_utente(session)
        if(utente_selezionato == None):
            return
        print(f"\n Utente selezionato {utente_selezionato.cognome} {utente_selezionato.nome} - {utente_selezionato.id}")

        # Seleziona la data odierna
        data_odierna = datetime.date.today()

        # Altri dati del prestito
        data_inizio = data_odierna
        data_fine = input_data_end()

        # Creazione dell'oggetto Prestito e aggiunta al database
        nuovo_prestito = Prestito(
            data_inizio=data_inizio,
            data_fine=data_fine,
            risorsa=risorsa_selezionata,
            utente=utente_selezionato,
        )

        # Controlla se esiste una prenotazione e chiudi se necessario
        prenotazione_da_modificare = check_prenotazione_exists(session, utente_selezionato, risorsa_selezionata)
        
        chiudi_prenotazione(session, prenotazione_da_modificare)

        add_object_opened_session(session, nuovo_prestito)

        print("Prestito aggiunto con successo.")

def check_prenotazione_exists(session, utente, risorsa):
    # Controlla se esiste una prenotazione dell'utente per la risorsa con stato "In attesa"
    prenotazione_da_modificare = session.query(Prenotazione).filter(
        Prenotazione.id_utente == utente.id,
        Prenotazione.id_risorsa == risorsa.id,
        Prenotazione.stato == "In attesa"
    ).first()

    return prenotazione_da_modificare

def chiudi_prenotazione(session, prenotazione):
    if prenotazione:
        # Se esiste una prenotazione, aggiorna lo stato a "Chiusa"
        prenotazione.stato = "Chiusa"
        session.commit()
        
def check_disponibilita_risorsa(session, id_risorsa):
    prestito_in_corso = session.query(Prestito).filter(
        Prestito.id_risorsa == id_risorsa,
        Prestito.data_consegna == None  # Verifica se la data di consegna è nulla
    ).first()

    if prestito_in_corso:
        #print(f"La risorsa è attualmente in prestito.")
        return False
    else:
        #print(f"La risorsa è disponibile per il prestito.")
        return True
    
def input_data_end():
    while True:
        data = input("\n Inserisci la data di fine prestito (formato YYYY-MM-DD): ").strip()
        if not data:
            print("Devi inserire una data valida.")
        elif not is_valid_date_format(data):
            print("Formato data non valido. Inserisci una data nel formato corretto (YYYY-MM-DD).")
        else:
            return data

def is_valid_date_format(date_string):
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False