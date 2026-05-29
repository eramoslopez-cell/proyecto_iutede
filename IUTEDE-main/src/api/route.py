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

from fastapi import APIRouter,Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import List

from src.infraestructure.database import get_db

from src.application.services import (RolService,UsuarioService)

from src.api.schemas import (RolCreate,RolResponse,UsuarioCreate,UsuarioResponse,UsuarioUpdate)

#api route que agrupa las rutas
#Asigna un versionamiento de nuestra API (en el futuro podemos utilizar por ejemplo v2 que seria la version 2 del api)

router = APIRouter(prefix="/API/V1")
alias_router = APIRouter()

#Rol 
@router.get("/roles", response_model=List[RolResponse], tags=["Roles"])
def listar_roles(db: Session = Depends(get_db)): #conexion a la base de datos
    return RolService(db).listar()



@router.get("/roles/{id_rol}", response_model=RolResponse, tags=["Roles"])
def obtener_rol(id_rol:int, db: Session=Depends(get_db)):
    rol = RolService(db).obtener(id_rol)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no ha sido encontrado")
    return rol

@router.post("/roles", response_model=RolResponse, status_code=status.HTTP_201_CREATED, tags=["Roles"])
def crear_rol(data:RolCreate, db: Session=Depends(get_db)):
    return RolService(db).crear(data.nombre_rol)

@router.delete("/roles/{id_rol}", status_code=status.HTTP_204_NO_CONTENT, tags=["Roles"])
def eliminar_rol(id_rol: int, db: Session = Depends(get_db)):
    if not RolService(db).eliminar(id_rol):
        raise HTTPException(status_code=404, detail="Rol no ha sido encontrado")
    #No hay necesidad de hacer return porque fast api detorna codigo 204 automaticamente
    
#Usuario
#ustedes basados en Rol crear Usuario
@router.get("/usuarios", response_model=List[UsuarioResponse], tags=["Usuarios"])
def listar_usuarios(db: Session = Depends(get_db)): #conexion a la base de datos
    return UsuarioService(db).listar()

@router.get("/usuarios/{id_usuario}", response_model=UsuarioResponse, tags=["Usuario"])
def obtener_usuario(id_usuario:int, db: Session=Depends(get_db)):
    usuario = UsuarioService(db).obtener(id_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no ha sido encontrado")
    return usuario

@router.post("/usuarios", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED, tags=["Usuarios"])
def crear_usuario(data:UsuarioCreate, db: Session=Depends(get_db)):
    if not RolService(db).obtener(data.id_rol):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El rol especificado no existe")
    try:
        return UsuarioService(db).crear(data.id_rol, data.nombre_completo, data.correo, data.contrasena_hash)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede crear el usuario. Verifique correo o datos duplicados.")

@router.delete("/usuarios/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT, tags=["Usuarios"])
def eliminar_usuario(id_usuario: int, db: Session = Depends(get_db)):
    if not UsuarioService(db).eliminar(id_usuario):
        raise HTTPException(status_code=404, detail="Usuario no ha sido encontrado")
    
@router.put("/usuarios/{id_usuario}", response_model=UsuarioResponse, tags=["Usuarios"])
def actualizar_usuario(id_usuario: int, data: UsuarioUpdate, db: Session = Depends(get_db)):
    #cuando hace el update solo actualiza los cambios que tuvieron cambios, lo demas no lo toca
    update_data = data.model_dump(exclude_none=True)
    if "id_rol" in update_data and not RolService(db).obtener(update_data["id_rol"]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El rol especificado no existe")
    try:
        usuario = UsuarioService(db).actualizar(id_usuario, **update_data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede actualizar el usuario. Verifique los datos.")
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# Alias routes without the /API/V1 prefix
@alias_router.get("/roles", response_model=List[RolResponse], tags=["Roles"])
def listar_roles_alias(db: Session = Depends(get_db)):
    return RolService(db).listar()

@alias_router.get("/roles/{id_rol}", response_model=RolResponse, tags=["Roles"])
def obtener_rol_alias(id_rol:int, db: Session=Depends(get_db)):
    rol = RolService(db).obtener(id_rol)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no ha sido encontrado")
    return rol

@alias_router.post("/roles", response_model=RolResponse, status_code=status.HTTP_201_CREATED, tags=["Roles"])
def crear_rol_alias(data:RolCreate, db: Session=Depends(get_db)):
    return RolService(db).crear(data.nombre_rol)

@alias_router.delete("/roles/{id_rol}", status_code=status.HTTP_204_NO_CONTENT, tags=["Roles"])
def eliminar_rol_alias(id_rol: int, db: Session = Depends(get_db)):
    if not RolService(db).eliminar(id_rol):
        raise HTTPException(status_code=404, detail="Rol no ha sido encontrado")

@alias_router.get("/usuarios", response_model=List[UsuarioResponse], tags=["Usuarios"])
def listar_usuarios_alias(db: Session = Depends(get_db)):
    return UsuarioService(db).listar()

@alias_router.get("/usuarios/{id_usuario}", response_model=UsuarioResponse, tags=["Usuario"])
def obtener_usuario_alias(id_usuario:int, db: Session=Depends(get_db)):
    usuario = UsuarioService(db).obtener(id_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no ha sido encontrado")
    return usuario

@alias_router.post("/usuarios", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED, tags=["Usuarios"])
def crear_usuario_alias(data:UsuarioCreate, db: Session=Depends(get_db)):
    if not RolService(db).obtener(data.id_rol):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El rol especificado no existe")
    try:
        return UsuarioService(db).crear(data.id_rol, data.nombre_completo, data.correo, data.contrasena_hash)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede crear el usuario. Verifique correo o datos duplicados.")

@alias_router.delete("/usuarios/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT, tags=["Usuarios"])
def eliminar_usuario_alias(id_usuario: int, db: Session = Depends(get_db)):
    if not UsuarioService(db).eliminar(id_usuario):
        raise HTTPException(status_code=404, detail="Usuario no ha sido encontrado")

@alias_router.put("/usuarios/{id_usuario}", response_model=UsuarioResponse, tags=["Usuarios"])
def actualizar_usuario_alias(id_usuario: int, data: UsuarioUpdate, db: Session = Depends(get_db)):
    update_data = data.model_dump(exclude_none=True)
    if "id_rol" in update_data and not RolService(db).obtener(update_data["id_rol"]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El rol especificado no existe")
    try:
        usuario = UsuarioService(db).actualizar(id_usuario, **update_data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede actualizar el usuario. Verifique los datos.")
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario
