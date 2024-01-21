from models.models import Prestito, Risorsa, Utente, Recensione
from methods.crud_generic import add_object_opened_session, add_object_to_database
from sqlalchemy.orm import joinedload
import datetime

def add_recensione(Session):
    with Session() as session:
        # Selezione del prestito a cui si riferisce la recensione
        prestito_selezionato = search_select_closed_prestito(session)
        
        if not prestito_selezionato:
            print("Nessun prestito chiuso trovato o scelta annullata.")
            return

        # Ottenimento delle informazioni sulla risorsa e sull'utente associati al prestito
        titolo_risorsa = prestito_selezionato.risorsa.titolo
        tipo_risorsa = prestito_selezionato.risorsa.tipo.descrizione
        nome_utente = prestito_selezionato.utente.nome
        cognome_utente = prestito_selezionato.utente.cognome

        print(f"Risorsa: {titolo_risorsa} ({tipo_risorsa})")
        print(f"Utente: {nome_utente} {cognome_utente}")

        # Chiedi all'utente di inserire il punteggio e la descrizione della recensione
        punteggio = input("Inserisci il punteggio (da 1 a 5): ").strip()
        descrizione = input("Inserisci una descrizione della recensione: ").strip()

        # Creazione dell'oggetto Recensione
        nuova_recensione = Recensione(
            punteggio=punteggio,
            descrizione=descrizione,
            id_prestito=prestito_selezionato.id
        )

        # Aggiunta della recensione al database
        add_object_opened_session(session, nuova_recensione)

        print("Recensione aggiunta con successo.")

# Funzione per cercare e selezionare un prestito chiuso
def search_select_closed_prestito(session):
    while True:
        search_id_utente = input("\nInserisci il nome dell'utente associato al prestito (lascia vuoto per ignorare): ").strip()
        search_id_risorsa = input("\nInserisci il titolo della risorsa associata al prestito (lascia vuoto per ignorare): ").strip()

        # Effettua la ricerca dei prestiti chiusi che corrispondono ai criteri
        query = session.query(Prestito).filter(Prestito.data_consegna != None)

        # Aggiungiamo una condizione per escludere i prestiti con recensioni
        query = query.outerjoin(Recensione, Prestito.id == Recensione.id_prestito).filter(Recensione.id == None)

        if search_id_utente:
            query = query.join(Prestito.utente).filter(Utente.nome.ilike(f"%{search_id_utente}%") | Utente.cognome.ilike(f"%{search_id_utente}%"))
        if search_id_risorsa:
            query = query.join(Prestito.risorsa).filter(Risorsa.titolo.ilike(f"%{search_id_risorsa}%"))

        prestiti_chiusi_trovati = query.all()

        if not prestiti_chiusi_trovati:
            print("\n Nessun prestito concluso trovato o tutti hanno già una recensione.")
            return None

        # Mostra i risultati della ricerca
        print("\nRisultati della ricerca Prestito Chiuso senza recensioni:")
        for i, prestito in enumerate(prestiti_chiusi_trovati):
            print(f"{i+1}. Risorsa: {prestito.risorsa.titolo}, Utente: {prestito.utente.nome} {prestito.utente.cognome}, Data di consegna: {prestito.data_consegna.strftime('%Y-%m-%d')}")

        scelta = input("\nSeleziona un prestito concluso (inserisci il numero) o 0 per annullare: ").strip()

        if scelta == "0":
            return None
        elif scelta.isdigit():
            scelta_prestito = int(scelta)
            if 1 <= scelta_prestito <= len(prestiti_chiusi_trovati):
                return prestiti_chiusi_trovati[scelta_prestito - 1]

        print("Scelta non valida. Riprova.")
        
def search_and_edit_recensioni(Session):
    with Session() as session: 
        while True:
            search_nome_cognome_utente = input("\nInserisci il nome o cognome dell'utente associato alla recensione (lascia vuoto per ignorare): ").strip()
            search_titolo_risorsa = input("Inserisci il titolo della risorsa associata alla recensione (lascia vuoto per ignorare): ").strip()

            # Effettua la ricerca delle recensioni che corrispondono ai criteri
            query = session.query(Recensione).filter_by(id_prestito=Prestito.id).join(Prestito).join(Utente, Prestito.utente).join(Risorsa, Prestito.risorsa)

            if search_nome_cognome_utente:
                # Applica il filtro sul campo del modello Utente
                query = query.filter(or_(Utente.nome.ilike(f"%{search_nome_cognome_utente}%"), Utente.cognome.ilike(f"%{search_nome_cognome_utente}%")))

            if search_titolo_risorsa:
                # Applica il filtro sul campo del modello Risorsa
                query = query.filter(Risorsa.titolo.ilike(f"%{search_titolo_risorsa}%"))

            recensioni_trovate = query.all()

            if not recensioni_trovate:
                print("Nessuna recensione trovata.")
                return None

            # Mostra i risultati della ricerca
            print("\nRisultati della ricerca Recensioni:")
            for i, recensione in enumerate(recensioni_trovate):
                prestito_associato = session.query(Prestito).filter_by(id=recensione.id_prestito).first()
                risorsa_associata = prestito_associato.risorsa
                utente_associato = prestito_associato.utente

                print(f"{i+1}. Utente: {utente_associato.nome} {utente_associato.cognome},")
                print(f"   Risorsa: ({risorsa_associata.genere.descrizione}) - {risorsa_associata.titolo}, {risorsa_associata.autore.nome} {risorsa_associata.autore.cognome}")
                print(f"   Recensione: {recensione.descrizione}")
                print(f"   Punteggio: {recensione.punteggio}")

            scelta = input("\nSeleziona una recensione (inserisci il numero) o 0 per annullare: ").strip()

            if scelta == "0":
                return None

            if scelta.isdigit():
                scelta_recensione = int(scelta)
                if 1 <= scelta_recensione <= len(recensioni_trovate):
                    recensione_da_modificare = recensioni_trovate[scelta_recensione - 1]
                    modifica_recensione(session, recensione_da_modificare)

# Funzione per la modifica di una recensione
def modifica_recensione(session, recensione):
    print("\n-- Modifica della Recensione --")
    prestito_associato = session.query(Prestito).filter_by(id=recensione.id_prestito).first()
    risorsa_associata = prestito_associato.risorsa
    utente_associato = prestito_associato.utente

    print(f"Utente: {utente_associato.nome} {utente_associato.cognome}")
    print(f"Titolo Risorsa: {risorsa_associata.titolo}")
    print(f"Descrizione attuale: {recensione.descrizione}")
    print(f"Punteggio attuale: {recensione.punteggio}")

    # Chiedi all'utente se vuole modificare qualche campo
    scelta_modifica = input("Vuoi modificare questa recensione? (s/n): ").strip().lower()
    if scelta_modifica != "s":
        return

    # Modifica della descrizione e del punteggio
    nuova_descrizione = input(f"Inserisci la nuova descrizione ({recensione.descrizione}): ").strip() or recensione.descrizione
    nuovo_punteggio = input(f"Inserisci il nuovo punteggio ({recensione.punteggio}): ").strip() or recensione.punteggio

    # Salva le modifiche
    recensione.descrizione = nuova_descrizione
    recensione.punteggio = nuovo_punteggio
    # Aggiunta della recensione al database
    add_object_opened_session(session, recensione)
    print("Recensione modificata con successo.")
    
