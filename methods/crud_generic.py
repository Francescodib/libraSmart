import models.models as mod

#generic function to add a new object to db
def add_object_to_database(Session,obj):
    with Session() as session:
        try:
            session.add(obj)
            session.commit()
            print(f"{obj.__repr__()} aggiunto correttamente al database")
        except Exception as e:
            session.rollback()
            print(f">>>Errore nell'aggiunta dell'oggetto al database: {e}")

#generic function to add a new object to db with opened session
def add_object_opened_session(session,obj):
    try:
        session.add(obj)
        session.commit()
        print(f"{obj.__tablename__.capitalize()} aggiunto correttamente al database")
    except Exception as e:
        session.rollback()
        print(f">>>Errore nell'aggiunta dell'oggetto al database: {e}")

def add_tipo(Session):
    print("\n-- Aggiungi un Nuovo Tipo di Risorsa --")
    while True:
        descr = input("Inserisci la descrizione del tipo: ").strip()
        # Verifica se la descrizione è stata inserita
        if descr:
            break
        else:
            print("Errore: la descrizione è obbligatoria. Riprova.")
    # Creazione dell'oggetto Tipo
    model = mod.Tipo(descrizione=descr)
    # Invio dati al metodo generico
    add_object_to_database(Session, model)
    
def find_edit_tipo(Session):
    print("\n-- Cerca e Seleziona un Tipo da modificare --")
    ricerca = input("Inserisci una descrizione da cercare: ").strip()

    with Session() as session:
        # Effettua la ricerca dei tipi di risorsa che corrispondono alla descrizione
        tipi_trovati = session.query(mod.Tipo).filter(mod.Tipo.descrizione.ilike(f"%{ricerca}%")).all()

        if not tipi_trovati:
            print("Nessun risultato trovato.")
            return None

        # Mostra i risultati della ricerca
        print("\n Risultati della ricerca:")
        for i, tipo in enumerate(tipi_trovati):
            print(f"{i+1}. {tipo.descrizione}")

        scelta = input("Seleziona un Tipo (inserisci il numero) o 0 per annullare: ").strip()

        if scelta == "0":
            return None
        elif scelta.isdigit():
            scelta_tipo = int(scelta)
            if 1 <= scelta_tipo <= len(tipi_trovati):
                tipo_selezionato = tipi_trovati[scelta_tipo - 1]
                print(f"\n-- Modifica Tipo di Risorsa: {tipo_selezionato.descrizione} --")
                nuova_descrizione = input("Inserisci la nuova descrizione del tipo: ").strip()
                tipo_selezionato.descrizione = nuova_descrizione
                session.commit()
                print("Tipo di risorsa aggiornato con successo.")
                return None

        print("Scelta non valida. Riprova.")
        return None

def find_edit_genere(Session):
    print("\n-- Cerca e Seleziona un Genere da modificare --")
    ricerca = input("Inserisci una descrizione da cercare: ").strip()

    with Session() as session:
        # Effettua la ricerca dei Generi di risorsa che corrispondono alla descrizione
        generi_trovati = session.query(mod.Genere).filter(mod.Genere.descrizione.ilike(f"%{ricerca}%")).all()

        if not generi_trovati:
            print("Nessun risultato trovato.")
            return None

        # Mostra i risultati della ricerca
        print("\nRisultati della ricerca:")
        for i, genere in enumerate(generi_trovati):
            print(f"{i+1}. {genere.descrizione}")

        scelta = input("Seleziona un Genere (inserisci il numero) o 0 per annullare: ").strip()

        if scelta == "0":
            return None
        elif scelta.isdigit():
            scelta_genere = int(scelta)
            if 1 <= scelta_genere <= len(generi_trovati):
                genere_selezionato = generi_trovati[scelta_genere - 1]
                print(f"\n-- Modifica Genere di Risorsa: {genere_selezionato.descrizione} --")
                nuova_descrizione = input("Inserisci la nuova descrizione del Genere: ").strip()
                genere_selezionato.descrizione = nuova_descrizione
                session.commit()
                print("Genere di risorsa aggiornato con successo.")
                return None

        print("Scelta non valida. Riprova.")
        return None

def find_edit_posizione(Session):
    print("\n-- Cerca e Seleziona una Posizione da modificare --")
    ricerca = input("Inserisci una descrizione da cercare: ").strip()

    with Session() as session:
        # Effettua la ricerca dei Generi di risorsa che corrispondono alla descrizione
        posizioni_trovate = session.query(mod.Posizione).filter(mod.Posizione.descrizione.ilike(f"%{ricerca}%")).all()

        if not posizioni_trovate:
            print("Nessun risultato trovato.")
            return None

        # Mostra i risultati della ricerca
        print("\nRisultati della ricerca:")
        for i, posizione in enumerate(posizioni_trovate):
            print(f"{i+1}. {posizione.descrizione}")

        scelta = input("Seleziona un Posizione (inserisci il numero) o 0 per annullare: ").strip()

        if scelta == "0":
            return None
        elif scelta.isdigit():
            scelta_posizione = int(scelta)
            if 1 <= scelta_posizione <= len(posizioni_trovate):
                posizione_selezionato = posizioni_trovate[scelta_posizione - 1]
                print(f"\n-- Modifica Posizione di Risorsa: {posizione_selezionato.descrizione} --")
                nuova_descrizione = input("Inserisci la nuova descrizione del Posizione: ").strip()
                posizione_selezionato.descrizione = nuova_descrizione
                session.commit()
                print("Posizione di risorsa aggiornato con successo.")
                return None

def find_edit_utente(Session):
    print("\n-- Cerca ed Edita Utente --")
    ricerca_cognome = input("Inserisci il cognome dell'utente da cercare (lascia vuoto per ignorare): ").strip()
    ricerca_nome = input("Inserisci il nome dell'utente da cercare (lascia vuoto per ignorare): ").strip()

    with Session() as session:
        # Costruisce la query in base ai campi inseriti
        query = session.query(mod.Utente)
        if ricerca_cognome:
            query = query.filter(mod.Utente.cognome.ilike(f"%{ricerca_cognome}%"))
        if ricerca_nome:
            query = query.filter(mod.Utente.nome.ilike(f"%{ricerca_nome}%"))

        utenti_trovati = query.all()

        if not utenti_trovati:
            print("Nessun utente trovato con i criteri specificati.")
            return

        # Mostra i risultati della ricerca
        print("\nRisultati della ricerca:")
        for i, utente in enumerate(utenti_trovati):
            print(f"{i+1}. {utente.nome} {utente.cognome}")

        scelta = input("Seleziona un utente (inserisci il numero) o 0 per annullare: ").strip()

        if scelta == "0":
            return

        elif scelta.isdigit():
            scelta_utente = int(scelta)
            if 1 <= scelta_utente <= len(utenti_trovati):
                utente_selezionato = utenti_trovati[scelta_utente - 1]

                print(f"\n-- Modifica Utente: {utente_selezionato.nome} {utente_selezionato.cognome} --")
                nuovo_nome = input(f"Inserisci il nuovo nome ({utente_selezionato.nome}): ").strip() or utente_selezionato.nome
                nuovo_cognome = input(f"Inserisci il nuovo cognome ({utente_selezionato.cognome}): ").strip() or utente_selezionato.cognome
                nuovo_email = input(f"Inserisci la nuova email ({utente_selezionato.email}): ").strip() or utente_selezionato.email
                nuovo_telefono = input(f"Inserisci il nuovo numero di telefono ({utente_selezionato.telefono}): ").strip() or utente_selezionato.telefono

                # Aggiorna i dati dell'utente nel database
                utente_selezionato.nome = nuovo_nome
                utente_selezionato.cognome = nuovo_cognome
                utente_selezionato.email = nuovo_email
                utente_selezionato.telefono = nuovo_telefono

                session.commit()

                print("Utente aggiornato con successo.")
                return

        print("Scelta non valida. Riprova.")

def add_genere(Session):
    print("\n-- Aggiungi un Nuovo Genere --")
    descr = input("Inserisci la descrizione del Genere: ")                                                                                                                      
    # Creazione dell'oggetto Tipo
    model = mod.Genere(descrizione=descr)
    # Invio dati al metodo generico
    add_object_to_database(Session,model)
    
def add_posizione(Session):
    print("\n-- Aggiungi un Nuova Posizione scaffale --")
    descr = input("Inserisci la descrizione della Posizione: ")                                                                                                                      
    # Creazione dell'oggetto Tipo
    model = mod.Posizione(descrizione=descr)
    # Invio dati al metodo generico
    add_object_to_database(Session,model)
    
def add_autore(Session):
    print("\n-- Aggiungi un Nuova Posizione scaffale --")
    cognome = input("Inserisci Cognome: ")
    nome = input("Inserisci Nome: ")                                                                                                                    
    # Creazione dell'oggetto Tipo
    model = mod.Autore(cognome=cognome,nome=nome)
    # Invio dati al metodo generico
    add_object_to_database(Session,model)
    
def add_utente(Session):
    print("\n-- Aggiungi un Nuovo Utente --")
    cognome = input("Inserisci Cognome: ")
    nome = input("Inserisci Nome: ") 
    email = input("Inserisci Email: ")  
    telefono = input("Inserisci Telefono:")                                                                                                                      
    # Creazione dell'oggetto Tipo
    model = mod.Utente(nome=nome,cognome=cognome,email=email,telefono=telefono)
    # Invio dati al metodo generico
    add_object_to_database(Session,model)
    
def conferma_operazione():
    conferma = input("Sei sicuro di voler procedere? (s/n): ").strip().lower()
    return conferma == "s"
    
#method for check if exsists
def exist_check(session,modello, **criteri):
    """
    Verifica se esiste un record in un dato modello basato su criteri specificati.

    Args:
        modello (Base): Il modello SQLAlchemy da interrogare.
        **criteri: Criteri di ricerca sotto forma di parole chiave.

    Returns:
        bool: True se esiste un record che corrisponde ai criteri, altrimenti False.
    """
    return session.query(modello).filter_by(**criteri).first() is not None