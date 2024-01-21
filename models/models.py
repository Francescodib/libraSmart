from sqlalchemy import Column, Integer, String, Date, ForeignKey, DECIMAL, Text
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.schema import UniqueConstraint


Base = declarative_base()

class Autore(Base):
    __tablename__ = 'autori'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    cognome = Column(String(100))
    def __repr__(self):
        return f"<Autore(Nome='{self.nome}', Cognome='{self.cognome}' id='{self.id}')>"

class Genere(Base):
    __tablename__ = 'generi'
    id = Column(Integer, primary_key=True)
    descrizione = Column(String(255), unique=True)
    def __repr__(self):
        return f"<Genere(descrizione='{self.descrizione}', id='{self.id}')>"

class Tipo(Base):
    __tablename__ = 'tipi'
    id = Column(Integer, primary_key=True)
    descrizione = Column(String(255), unique=True)
    def __repr__(self):
        return f"<Tipo(descrizione='{self.descrizione}', id='{self.id}')>"
    
class Posizione(Base):
    __tablename__ = 'posizioni'
    id = Column(Integer, primary_key=True)
    descrizione = Column(String(255), unique=True)
    def __repr__(self):
        return f"<Posizione(descrizione='{self.descrizione}', id='{self.id}')>"

class Risorsa(Base):
    __tablename__ = 'risorse'
    id = Column(Integer, primary_key=True)
    titolo = Column(String(255))
    edizione = Column(String(100))
    id_autore = Column(Integer, ForeignKey('autori.id'))
    id_genere = Column(Integer, ForeignKey('generi.id'))
    id_tipo = Column(Integer, ForeignKey('tipi.id'))
    anno_pubblicazione = Column(Integer)
    condizioni = Column(String(255))
    id_posizione = Column(Integer, ForeignKey('posizioni.id'))
    # Relazioni
    autore = relationship("Autore")
    genere = relationship("Genere")
    tipo = relationship("Tipo")
    posizione = relationship("Posizione")
    prestiti = relationship("Prestito", back_populates="risorsa")

class Utente(Base):
    __tablename__ = 'utenti'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    cognome = Column(String(100))
    email = Column(String(255), unique=True)
    telefono = Column(String(20))
    # Relazioni
    prestiti = relationship("Prestito", back_populates="utente")
    # Vincolo UNIQUE su cognome e nome
    __table_args__ = (UniqueConstraint('cognome', 'nome', name='_cognome_nome_uc'),)

class Prestito(Base):
    __tablename__ = 'prestiti'
    id = Column(Integer, primary_key=True)
    data_inizio = Column(Date)
    data_fine = Column(Date)
    data_consegna = Column(Date)
    id_risorsa = Column(Integer, ForeignKey('risorse.id'))
    id_utente = Column(Integer, ForeignKey('utenti.id'))
    # Relazioni
    risorsa = relationship("Risorsa", back_populates="prestiti")
    utente = relationship("Utente", back_populates="prestiti")

class Prenotazione(Base):
    __tablename__ = 'prenotazioni'
    id = Column(Integer, primary_key=True)
    data = Column(Date)
    stato = Column(String(100))
    id_risorsa = Column(Integer, ForeignKey('risorse.id'))
    id_utente = Column(Integer, ForeignKey('utenti.id'))

class Sanzione(Base):
    __tablename__ = 'sanzioni'
    id = Column(Integer, primary_key=True)
    importo = Column(DECIMAL(10, 2))
    descrizione = Column(String(255))
    id_prestito = Column(Integer, ForeignKey('prestiti.id'))

class Recensione(Base):
    __tablename__ = 'recensioni'
    id = Column(Integer, primary_key=True)
    punteggio = Column(Integer)
    descrizione = Column(Text)
    id_prestito = Column(Integer, ForeignKey('prestiti.id'))
