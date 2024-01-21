from models.models import *
from methods.crud_generic import add_object_to_database

# Creazione e aggiunta di oggetti alle sole tabelle senza vincoli esterni
def popola_database(Session):
    # Autori
    autori = [
        Autore(nome='Giovanni', cognome='Boccaccio'),
        Autore(nome='Dante', cognome='Alighieri'),
        Autore(nome='William', cognome='Shakespeare'),
        Autore(nome='Jane', cognome='Austen'),
        Autore(nome='Leo', cognome='Tolstoy')
    ]

    for autore in autori:
        add_object_to_database(Session, autore)

    # Generi
    generi = [
        Genere(descrizione='Romanzo'),
        Genere(descrizione='Poesia'),
        Genere(descrizione='Storia'),
        Genere(descrizione='Fantascienza'),
        Genere(descrizione='Saggio')
    ]

    for genere in generi:
        add_object_to_database(Session, genere)

    # Tipi
    tipi = [
        Tipo(descrizione='Libro'),
        Tipo(descrizione='Rivista'),
        Tipo(descrizione='CD'),
        Tipo(descrizione='DVD'),
        Tipo(descrizione='Audiolibro')
    ]

    for tipo in tipi:
        add_object_to_database(Session, tipo)

    # Posizioni
    posizioni = [
        Posizione(descrizione='Scaffale 1'),
        Posizione(descrizione='Scaffale 2'),
        Posizione(descrizione='Scaffale 3'),
        Posizione(descrizione='Scaffale 4'),
        Posizione(descrizione='Scaffale 5')
    ]

    for posizione in posizioni:
        add_object_to_database(Session, posizione)

    # Utenti
    utenti = [
        Utente(nome='Mario', cognome='Rossi', email='mario.rossi@email.it', telefono='1234567890'),
        Utente(nome='Luigi', cognome='Verdi', email='luigi.verdi@email.it', telefono='0987654321'),
        Utente(nome='Anna', cognome='Bianchi', email='anna.bianchi@email.it', telefono='2345678901'),
        Utente(nome='Giulia', cognome='Neri', email='giulia.neri@email.it', telefono='3456789012'),
        Utente(nome='Marco', cognome='Gialli', email='marco.gialli@email.it', telefono='4567890123')
        ]

    for utente in utenti:
        add_object_to_database(Session, utente)
        
# Da richiamare solo dopo aver popolato le tabelle senza Forein Key
def popola_tabelle_con_dipendenze(Session):
    # Assumiamo che le tabelle Autori, Generi, Tipi, Posizioni e Utenti siano già state popolate

    # Risorse
    risorse = [
        Risorsa(titolo='Il Decameron', edizione='1a Edizione', id_autore=1, id_genere=1, id_tipo=1, anno_pubblicazione=1353, condizioni='Nuovo', id_posizione=1),
        Risorsa(titolo='La Divina Commedia', edizione='2a Edizione', id_autore=2, id_genere=2, id_tipo=1, anno_pubblicazione=1320, condizioni='Copertina rovinata', id_posizione=2),
        Risorsa(titolo='Romeo e Giulietta', edizione='3a Edizione', id_autore=3, id_genere=1, id_tipo=2, anno_pubblicazione=1597, condizioni='Buono', id_posizione=3),
        Risorsa(titolo='Orgoglio e Pregiudizio', edizione='1a Edizione', id_autore=4, id_genere=1, id_tipo=3, anno_pubblicazione=1813, condizioni='Nuovo', id_posizione=4),
        Risorsa(titolo='Guerra e Pace', edizione='2a Edizione', id_autore=5, id_genere=1, id_tipo=4, anno_pubblicazione=1869, condizioni='Ingiallito', id_posizione=5)
    ]

    for risorsa in risorse:
        add_object_to_database(Session, risorsa)

    # Prestiti
    prestiti = [
        Prestito(data_inizio='2024-01-01', data_fine='2024-01-31', data_consegna='2024-01-30', id_risorsa=1, id_utente=1),
        Prestito(data_inizio='2024-01-02', data_fine='2024-01-28', data_consegna='2024-01-27', id_risorsa=2, id_utente=2),
        Prestito(data_inizio='2024-01-01', data_fine='2024-01-31', data_consegna=None, id_risorsa=3, id_utente=3),
        Prestito(data_inizio='2024-01-01', data_fine='2024-01-30', data_consegna=None, id_risorsa=4, id_utente=4)
    ]

    for prestito in prestiti:
        add_object_to_database(Session, prestito)

    # Prenotazioni
    prenotazioni = [
        Prenotazione(data='2024-01-01', stato='In attesa', id_risorsa=1, id_utente=2),
        Prenotazione(data='2024-01-01', stato='In attesa', id_risorsa=2, id_utente=3),
    ]

    for prenotazione in prenotazioni:
        add_object_to_database(Session, prenotazione)

    # Sanzioni
    sanzioni = [
        Sanzione(importo=5.00, descrizione='Ritardo nella restituzione', id_prestito=1)
        ]

    for sanzione in sanzioni:
        add_object_to_database(Session, sanzione)

    # Recensioni
    recensioni = [
        Recensione(punteggio=4, descrizione='Ottima lettura, consigliato!', id_prestito=1)
    ]

    for recensione in recensioni:
        add_object_to_database(Session, recensione)
