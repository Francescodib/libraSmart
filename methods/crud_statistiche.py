from sqlalchemy import func
from models.models import Prestito,Prenotazione,Risorsa,Recensione,Utente,Sanzione

def stat_call(Session,req):
    with Session() as session:
        if req=="ris_richieste":
            top_10_risorse_richieste(session)
        elif req =="ris_voto":
            top_10_risorse_voto(session)
        elif req =="ute_sanzioni":
            top_10_utenti_sanzioni(session)
        else:
            print("Selezione non valida.")
            return    
        

def top_10_risorse_richieste(session):
    result = session.query(Risorsa, func.count(Prestito.id)).\
        join(Prestito, Prestito.id_risorsa == Risorsa.id).\
        group_by(Risorsa.id).\
        order_by(func.count(Prestito.id).desc()).\
        limit(10).all()

    if not result:
        print("Nessuna risorsa trovata.")
        return

    print("Le 10 risorse più richieste sono:")
    for i, (risorsa, count) in enumerate(result):
        print(f"{i+1}. Titolo: {risorsa.titolo}, Numero di prestiti: {count}")

def top_10_risorse_voto(session):
    result = session.query(Risorsa, func.avg(Recensione.punteggio)).\
        join(Prestito, Prestito.id_risorsa == Risorsa.id).\
        join(Recensione, Recensione.id_prestito == Prestito.id).\
        group_by(Risorsa.id).\
        order_by(func.avg(Recensione.punteggio).desc()).\
        limit(10).all()

    if not result:
        print("Nessuna risorsa trovata.")
        return

    print("Le 10 risorse più votate sono:")
    for i, (risorsa, avg_punteggio) in enumerate(result):
        print(f"{i+1}. Titolo: {risorsa.titolo}, Voto Medio: {avg_punteggio:.2f}")
        

def top_10_utenti_sanzioni(session):
    result = session.query(Utente, func.count(Sanzione.id)).\
        join(Prestito, Prestito.id_utente == Utente.id).\
        join(Sanzione, Sanzione.id_prestito == Prestito.id).\
        group_by(Utente.id).\
        order_by(func.count(Sanzione.id).desc()).\
        limit(10).all()

    if not result:
        print("Nessun utente trovato.")
        return

    print("I 10 utenti con più sanzioni sono:")
    for i, (utente, count) in enumerate(result):
        print(f"{i+1}. Nome: {utente.nome}, Cognome: {utente.cognome}, Numero di Sanzioni: {count}")