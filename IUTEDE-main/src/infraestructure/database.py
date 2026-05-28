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
#esto evita tener que escribir las variables directamente

#esta es la cadena de conexion
DATABASE_URL = (f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME')}")

#creamos el Engine 
engine = create_engine(DATABASE_URL,pool_pre_ping=True)

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