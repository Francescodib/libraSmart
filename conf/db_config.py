from sqlalchemy import create_engine

USER = 'root'
PASSWORD = ''  # Password da impostare se necessario
HOST = 'localhost'
PORT = '3306'

DB_NAME = 'LibraSmart_DB'

ENGINE_URL = f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
db_engine = create_engine(ENGINE_URL, echo=False)