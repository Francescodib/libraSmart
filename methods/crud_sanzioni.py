from models.models import Sanzione, Prestito, Utente, Risorsa
from methods.crud_generic import add_object_opened_session
from sqlalchemy import or_

def add_sanzione(Session):
    with Session() as session:
        # Selezione del prestito a cui si riferisce la sanzione
        prestito_selezionato = search_sel_prestito_wo_sanzione(session)

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


def search_sel_prestito_wo_sanzione(session):
    while True:
        search_id_utente = input("\nInserisci il nome dell'utente associato al prestito (lascia vuoto per ignorare): ").strip()
        search_id_risorsa = input("Inserisci il titolo della risorsa associata al prestito (lascia vuoto per ignorare): ").strip()

        # Effettua la ricerca dei prestiti chiusi che corrispondono ai criteri
        query = session.query(Prestito).filter(Prestito.data_consegna != None)

        # Aggiungiamo una condizione per escludere i prestiti con Sanzioni
        query = query.outerjoin(Sanzione, Prestito.id == Sanzione.id_prestito).filter(Sanzione.id == None)

        if search_id_utente:
            query = query.join(Prestito.utente).filter(Utente.nome.ilike(f"%{search_id_utente}%") | Utente.cognome.ilike(f"%{search_id_utente}%"))
        if search_id_risorsa:
            query = query.join(Prestito.risorsa).filter(Risorsa.titolo.ilike(f"%{search_id_risorsa}%"))

        prestiti_chiusi_trovati = query.all()

        if not prestiti_chiusi_trovati:
            print("\nNessun prestito Chiuso trovato o tutti hanno già una Sanzione registrata.")
            return None

        # Mostra i risultati della ricerca
        print("\nRisultati della ricerca Prestito Chiuso senza Sanzioni:")
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

def search_and_edit_sanzioni(Session):
    with Session() as session:
        while True:
            search_nome_cognome_utente = input("\nInserisci il nome o cognome dell'utente associato alla sanzione (lascia vuoto per ignorare): ").strip()

            # Effettua la ricerca delle sanzioni che corrispondono ai criteri
            query = session.query(Sanzione).join(Prestito).join(Utente).join(Risorsa)

            if search_nome_cognome_utente:
                # Applica il filtro sul campo del modello Utente
                query = query.filter(or_(Utente.nome.ilike(f"%{search_nome_cognome_utente}%"), Utente.cognome.ilike(f"%{search_nome_cognome_utente}%")))

            sanzioni_trovate = query.all()

            if not sanzioni_trovate:
                print("Nessuna sanzione trovata.")
                return None

            # Mostra i risultati della ricerca
            print("\nRisultati della ricerca Sanzioni:")
            for i, sanzione in enumerate(sanzioni_trovate):
                prestito_associato = session.query(Prestito).filter_by(id=sanzione.id_prestito).first()
                risorsa_associata = prestito_associato.risorsa
                utente_associato = prestito_associato.utente

                print(f"{i+1}. Utente: {utente_associato.nome} {utente_associato.cognome},")
                print(f"   Risorsa: ({risorsa_associata.genere.descrizione}) - {risorsa_associata.titolo}, {risorsa_associata.autore.nome} {risorsa_associata.autore.cognome}")
                print(f"   Importo: {sanzione.importo}")
                print(f"   Descrizione: {sanzione.descrizione}")

            scelta = input("\nSeleziona una sanzione (inserisci il numero) o 0 per annullare: ").strip()

            if scelta == "0":
                return None

            if scelta.isdigit():
                scelta_sanzione = int(scelta)
                if 1 <= scelta_sanzione <= len(sanzioni_trovate):
                    sanzione_da_modificare = sanzioni_trovate[scelta_sanzione - 1]
                    edit_sanzione(session, sanzione_da_modificare)

def edit_sanzione(session, sanzione):
    print("\n-- Modifica della Sanzione --")
    prestito_associato = session.query(Prestito).filter_by(id=sanzione.id_prestito).first()
    risorsa_associata = prestito_associato.risorsa
    utente_associato = prestito_associato.utente

    print(f"Utente: {utente_associato.nome} {utente_associato.cognome}")
    print(f"Risorsa: ({risorsa_associata.genere.descrizione}) - {risorsa_associata.titolo}")
    print(f"Importo attuale: {sanzione.importo}")
    print(f"Descrizione attuale: {sanzione.descrizione}")

    # Chiedi all'utente se vuole modificare qualche campo
    scelta_modifica = input("Vuoi modificare questa sanzione? (s/n): ").strip().lower()
    if scelta_modifica != "s":
        return

    # Modifica dell'importo e della descrizione
    nuovo_importo = input(f"Inserisci il nuovo importo ({sanzione.importo}): ").strip() or sanzione.importo
    nuova_descrizione = input(f"Inserisci la nuova descrizione ({sanzione.descrizione}): ").strip() or sanzione.descrizione

    # Salva le modifiche
    sanzione.importo = nuovo_importo
    sanzione.descrizione = nuova_descrizione
    add_object_opened_session(session,sanzione)