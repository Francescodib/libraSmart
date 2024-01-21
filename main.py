from sqlalchemy.orm import sessionmaker
from menu.menu import main_menu
from conf import db_config

"""
 ▍█▞ LibraSm@rt ▞█ ▍ v1.0 - Applicativo per Gestione Bibliotecaria

Realizzato a completamento dell'E-tivity N.4 dell'esame "Basi di Dati" 

Autore: Francesco di Biase
Matricola: IN08000245


Questo è il file principale dell'applicativo LibraSmart. 
LibraSmart utilizza Python insieme alle librerie MySQL-connector-python ed SQLAlchemy come ORM per gestire in modo efficiente i dati.

Caratteristiche principali:
- Gestione delle risorse bibliotecarie (libri, riviste, DVD, audiolibri, etc.).
- Gestione
- Controllo dei prestiti e delle prenotazioni per garantire una corretta gestione delle risorse.
- Gestione degli utenti e dei loro dati.
- Implementazione di operazioni CRUD per tutte le entità del sistema.
- Gestione accurata degli errori e messaggi di errore esplicativi.
- Generazione di classifiche e statistiche basiche per il monitoraggio delle attività della biblioteca.
- Ricerca avanzata per trovare rapidamente le risorse desiderate, controllare la loro disponibilità, la posizione sullo scaffale, etc.
- Rigorosi vincoli di integrità dei dati per mantenere la coerenza delle informazioni.

L'interfaccia utente è basata su una semplice interfaccia a riga di comando (CLI) che garantisce una facile interazione con tutte le funzionalità offerte da LibraSmart.

Informazioni importanti per il primo avvio:
- La configurazione del database va impostata nel file conf/db_config.py
- Le funzioni del menu alla voce 1.Gestione Database permettono la creazione del db con il nome di default "librasmart_db", la creazione delle tabelle, ed la creazione di dati di esempio per consentire un veloce utilizzo di prova.
- Nello stesso sottomenù è presente una funzione per effettuare il reset del Database che consente un avvio pulito in caso di utilizzo con dati reali.
- Tutte le funzioni critiche per i dati richiedono il consenso dell'operatore per proseguire.

Per avviare l'applicativo, esegui questo file utilizzando il seguente comando:

    python main.py

"""

# Database config from conf/db_config.py
Session = sessionmaker(bind=db_config.db_engine)

if __name__ == "__main__":
    main_menu(Session)