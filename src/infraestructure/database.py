#la conexion a la base de datos y el repositorio
#establecer la base de datos
#MYSQL usando SQLAlchemy como nuestro ORM (object-relational mapping)
#convierte tablas de sql a clases de pthyon

# conceptos claves
#Engine: representa la conexion fisica al motor de la base de datos
#Sesion: unidad de trabajo acomula operaciones antes de enviarla a la base de datos
#Base: clase padre de la cual heredam todos los modelos del ORM

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

#cargar las variables definidas en el archivo .env al entorno del proceso
load_dotenv()
if os.path.exists('env'):
    load_dotenv('env')
#esto evita tener que escribir las variables directamente

# leer configuración de base de datos
_db_user = os.getenv('DB_USER')
_db_password = os.getenv('DB_PASSWORD')
_db_host = os.getenv('DB_HOST')
_db_port = os.getenv('DB_PORT', '3306')
_db_name = os.getenv('DB_NAME')


def _is_missing(value: str | None) -> bool:
    return value is None or value.strip() == '' or value.strip().lower() == 'none'


if _is_missing(_db_user) or _is_missing(_db_password) or _is_missing(_db_host) or _is_missing(_db_name):
    DATABASE_URL = 'sqlite:///./local.db'
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    DATABASE_URL = (
        f"mysql+pymysql://{_db_user}:{_db_password}"
        f"@{_db_host}:{_db_port}/{_db_name}"
    )
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

#creamos la sesion
sesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#declaramos la base
#Heredar todos los modelos del ORM
class Base(DeclarativeBase):
    pass

#utilizamos un generador que provee una sesion de db a cada enpoint de fastapo
#get_db

def get_db():
    db = sesionLocal()  # abre una nueva sesión
    try:
        yield db  # entrega la sesión al endpoint que la solicitó
    finally:
        db.close()  # cierra la sesión