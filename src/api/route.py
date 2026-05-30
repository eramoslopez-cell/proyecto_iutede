#rutas de los endpoints de la api
#Aqui estan definidos los endpoints HTTP
#es la capa mas externa de nuestro modelo
#es la que recibe las peticiones
#y es la que retorna los datos

#metodos HTTP usados
#GET ->Leer/consulta los datos (SELECT)
#POST -> Crear un nuevo recurso/ (INSERT)
#PUT -> Reemplazar un recurso completo (UPDATE)
#PATCH -> modifica parcialmente un recurso es como un update
#DELETE -> Elimina un recurso (DELETE)

#codigos de estado HTTP:
# 200 OK GET - PUT - PATCH son exitosos
#201 created -> POST exitoso
#204 No content -> Delete exitoso
#404 Not Found -> El recurso solicitado no existe 
#Depends(get_db):
#FastAPI inyecta automaticamente una sesion de la base de datos a cada endpoind

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.infraestructure.database import get_db

from src.application.services import (RolService, UsuarioService)

from src.api.schemas import (RolCreate, RolResponse, UsuarioCreate, UsuarioResponse, UsuarioUpdate)

#APIRouter, que agrupa las rutas 
#Asigna un versionamiento de nuestra API (en el futuro podemos utilizar por ejemplo el v2)
router = APIRouter(prefix="/api/v1")

#Rol 
@router.get("/roles", response_model=List[RolResponse], tags=["Roles"])
def listar_roles(db: Session = Depends(get_db)):
    return RolService(db).listar()

@router.get("/roles/{rol_id}", response_model=RolResponse, tags=["Roles"])
def obtener_rol(rol_id: int, db: Session=Depends(get_db)):
    rol = RolService(db).obtener(rol_id)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol
    
@router.post("/roles", response_model=RolResponse, status_code=status.HTTP_201_CREATED, tags=["Roles"])
def crear_rol(rol: RolCreate, db: Session=Depends(get_db)):
    return RolService(db).crear(rol.nombre_rol)

@router.delete("/roles/{rol_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Roles"])
def eliminar_rol(rol_id: int, db: Session = Depends(get_db)):
    if not RolService(db).eliminar(rol_id):
        raise HTTPException(status_code=404, detail="Rol no encontrado")
#no hay necesidad de hacer return porque FastAPI retorna automaticamente

#Usuario
#ustedes basados  en Rol crear usuario 
@router.get("/usuarios", response_model=List[UsuarioResponse], tags=["Usuarios"])
def listar_usuarios(db: Session = Depends(get_db)):
    return UsuarioService(db).listar()

@router.get("/usuarios/{usuario_id}", response_model=UsuarioResponse, tags=["Usuarios"])
def obtener_usuario(usuario_id: int, db: Session=Depends(get_db)):
    usuario = UsuarioService(db).obtener(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.post("/usuarios", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED, tags=["Usuarios"])
def crear_usuario(usuario: UsuarioCreate, db: Session=Depends(get_db)):
    return UsuarioService(db).crear(usuario.id_rol, usuario.nombre_completo, usuario.correo, usuario.contrasena_hash)

@router.delete("/usuarios/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Usuarios"])
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    if not UsuarioService(db).eliminar(usuario_id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
@router.put("/usuarios/{id_usuario}", response_model=UsuarioResponse, tags=["Usuarios"])
def actualizar_usuario(id_usuario: int, data: UsuarioUpdate, db: Session = Depends(get_db)):
    usuario = UsuarioService(db).actualizar(id_usuario, **data.dict(exclude_none=True))
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


