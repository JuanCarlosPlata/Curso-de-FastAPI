import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base # este nos sirve para manipular todas las tables de nuestra base de datos

# aquí guardaremos el nombre de la base de datos
sqlite_file_name = "../database.sqlite"
# lo que hace lo siguiente es leer el directorio actual de este archivo que es database.py
base_dir = os.path.dirname(os.path.realpath(__file__))
# usando :/// es la forma de conectarse a una base de datos sqlite
database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"
# representa el motor de la base de datos
engine = create_engine(database_url, echo=True)
# esta variable permite crear una session para conectarse a la base de datos
Session = sessionmaker(bind=engine)

Base = declarative_base()