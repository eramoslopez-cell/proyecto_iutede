#casos de uso del sistema
#Los servicios contienen la logica del negocio
#saben que hacer, pero le delegan a los repositorios como hacer el CRUD

#responsabilidad de esta capa
#orquestar la comunicacion con los repositorios
#aplicar las reglas de negocio ( ej: una reserva de un laboratorio, )
#solo se aprueba si esta pendiente
#transformar los datos antes de retornalos al API

#capa API = recibir las peticiones HTTP
#servicio = aplica la logica del negocio
#repositorio = Ejecute las consultas SQL CRUD
#infraestructura = no es conocida por el API

from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from src.domain.models import(Roles, Usuario, Estudiante, Profesor, Recursos)

from src.infraestructure.repository import(RolRepository, UsuarioRepository, BaseRepository)

#Rol Service
class RolService:
    def __init__(self, db:Session):
        #creamos una instancia del repositorio pasando la sesion de la base de datos
        self.repo = RolRepository(db)

    def listar(self)-> List[Roles]:
        return self.repo.get_all()

    def obtener(self, id_rol:int) -> Optional[Roles]:
        return self.repo.get_by_id(id_rol)

    def crear(self, nombreRol:str) ->Roles: #crea el objeto en memoria
        return self.repo.create(Roles(nombre_rol=nombreRol)) #entrega al repo para que haga el insert

    def eliminar(self,id_rol:int) ->bool:
        return self.repo.delete(id_rol)

#Usuario service
class UsuarioService:
    def __init__(self, db:Session):
        #creamos una instancia del repositorio pasando la sesion de la base de datos
        self.repo = UsuarioRepository(db)

    def listar(self)-> List[Usuario]:
        return self.repo.get_all()

    def obtener(self, id_usuario:int) -> Optional[Usuario]:
        return self.repo.get_by_id(id_usuario)

    def obtenerNombre(self, nombre_usuario:str) -> Optional[Usuario]:
        return self.repo.get_by_nombre_completo(nombre_usuario)

    def obtenerCorreo(self, correo:str) -> Optional[Usuario]:
        return self.repo.get_by_correo(correo)

    def crear(self, id_rol:int, nombre_completo: str, correo: str, password: str) ->Usuario: #crea el objeto en memoria
        newUsuario = Usuario(
            id_rol = id_rol,
            nombre_completo = nombre_completo,
            correo = correo,
            contrasena_hash = password
        )
        return self.repo.create(newUsuario) #entrega al repo para que haga el insert

    def actualizar(self, id_usuario:int, **kwargs) -> Optional[Usuario]:
        usuario = self.repo.get_by_id(id_usuario)
        if not usuario:
            return None
        for key, value in kwargs.items():
            setattr(usuario, key, value)
        return self.repo.update(usuario)

    def eliminar(self,id_usuario:int) ->bool:
        return self.repo.delete(id_usuario)