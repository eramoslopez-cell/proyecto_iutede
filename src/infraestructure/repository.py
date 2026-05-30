#los CRUD
#El repositorio encapsula las consultas sql
#solo sabe guardar, recuperar, eliminar y modificar los datos
#pero no sabe porque

from typing import Optional, List, Type, TypeVar
from sqlalchemy.orm import Session
from src.domain.models import(Roles, Usuario, Estudiante, Profesor, Monitor)

#se usa para que el tipo de retorno de los archivos genericos sean consistentes
#con el modelo(Rol,Usuario,Estudiante, etc)
T = TypeVar("T")

#clase Base con las operaciones genericas del crud
#Insert, Select, Delete, Update

class BaseRepository:
    def __init__(self, model: Type[T], db: Session):
        #model: es la clase del ORM (Rol,Usuario,Estudiante etc)
        #db: la sesion de conexion a la base de datos
        self.model = model
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def get_by_id(self, record_id: int) -> Optional[T]:
        pk = self.model.__mapper__.primary_key[0].name
        return self.db.query(self.model).filter(getattr(self.model, pk) == record_id).first()

    def create(self, obj: T) -> T:
        self.db.add(obj) #Añadir el objeto a la sesion, aun no esta en la base de datos
        self.db.commit() #Enviamos el insert a la base de datos y se confirma
        self.db.refresh(obj) #Recargar el objeto desde la base de datos
        return obj

    def update(self, obj: T) -> T:
        self.db.commit() #Enviamos el update a la base de datos y se confirma
        self.db.refresh(obj) #Recargar el objeto desde la base de datos
        return obj

    def delete(self, record_id: int) -> bool:
        obj = self.get_by_id(record_id)
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True

#metodos especificos

class RolRepository(BaseRepository):
    def __init__(self, db:Session):
        super().__init__(Roles, db)

    def get_by_nombre(self, nombre:str) -> Optional[Roles]:
        return self.db.query(Roles).filter(Roles.nombre_rol == nombre).first()

class UsuarioRepository(BaseRepository):
    def __init__(self, db:Session):
        super().__init__(Usuario, db)

    def get_by_nombre_completo(self,nombre:str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.nombre_completo == nombre).first()

    def get_by_correo(self, correo:str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.correo == correo).first()
        
        
        
        
       