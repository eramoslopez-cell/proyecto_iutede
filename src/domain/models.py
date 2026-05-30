#capa de dominio(entidades y reglas de negocio)
#es como un espejo que comunica db con python
#una tabla equivale a una clase

from datetime import datetime
from typing import Optional, List
from sqlalchemy import Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import mapped_column, Mapped, relationship

#importamos la clase base desde la capa de infraestructura
from src.infraestructure.database import Base

#=========================
#RQL
#=========================
class Roles(Base):
    __tablename__ = "ROLES"
#primary key, autoincrementable
    id_rol: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre_rol: Mapped[str] = mapped_column(String(50))
    
    #Relacion inversa: Desde rol podemos acceder a la lista de usuarios
    usuarios: Mapped[List["Usuario"]] = relationship("Usuario", back_populates="rol")
     

#=========================
#RQL
#=========================

class Usuario(Base):
    __tablename__ = "USUARIOS"
    id_usuario: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    #FK heredada de la tabla roles el id rol
    id_rol: Mapped[int] = mapped_column(ForeignKey("ROLES.id_rol"))
    nombre_completo: Mapped[str] = mapped_column(String(150))
    correo: Mapped[str] = mapped_column(String(100), unique=True)
    contrasena_hash: Mapped[str] = mapped_column(String(255))
    
    #Relacion hacia la tabla ROLES y hacia las tablas hijas 
    rol: Mapped["Roles"] = relationship("Roles", back_populates="usuarios")
    
    estudiante: Mapped[Optional["Estudiante"]] = relationship("Estudiante", back_populates="usuario", uselist=False)
    profesor: Mapped[Optional["Profesor"]] = relationship("Profesor", back_populates="usuario", uselist=False)
    monitor: Mapped[Optional["Monitor"]] = relationship("Monitor", back_populates="usuario", uselist=False)

#=========================
#Estudiante
#=========================
class Estudiante(Base):
    __tablename__ = "ESTUDIANTES"
#al ser pk y fk al mismo tiempo, en este caso se vincula al estudiante con el usuario
    id_usuario: Mapped[int] = mapped_column(ForeignKey("USUARIOS.id_usuario"), primary_key=True)
    matricula: Mapped[str] = mapped_column(String(50), unique=True)
    programa: Mapped[str] = mapped_column(String(100))
    
    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="estudiante")
    
#profesor
#monitor
#recurso

class Profesor(Base):
    __tablename__ = "PROFESORES"
    id_usuario: Mapped[int] = mapped_column(ForeignKey("USUARIOS.id_usuario"), primary_key=True)
    departamento: Mapped[str] = mapped_column(String(100))
    
    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="profesor")
    

class Monitor(Base):
    __tablename__ = "MONITORES"
    id_usuario: Mapped[int] = mapped_column(ForeignKey("USUARIOS.id_usuario"), primary_key=True)
    id_turno: Mapped[int] = mapped_column(Integer)
    
    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="monitor")
    reservas: Mapped[List["Reservas"]] = relationship("Reservas", back_populates="monitor")
    prestamos: Mapped[List["Prestamos"]] = relationship("Prestamos", back_populates="monitor")
    
    
    #monitor gestiona las reservas
    #monitor tiene que ver con los prestamos
    
    #Recurso esta relacionado
    #laboratorio
    #equipos portatiles
    
    #Reservas
    #Equipos_portatiles
    #novedades

class Recursos(Base):
    __tablename__ = "RECURSOS"
    id_recurso: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_placa: Mapped[str] = mapped_column(ForeignKey("PLACAS.id_placa"))
    
    laboratorios: Mapped[List["Laboratorios"]] = relationship("Laboratorios", back_populates="recursos")
    reservas: Mapped[List["Reservas"]] = relationship("Reservas", back_populates="recurso")
    

    
class Reservas(Base):
    __tablename__ = "RESERVAS"
    id_reserva: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_usuario_solicita: Mapped[int] = mapped_column(ForeignKey("USUARIOS.id_usuario"))
    id_recurso: Mapped[int] = mapped_column(ForeignKey("RECURSOS.id_recurso"))
    id_monitor_aprueba: Mapped[int] = mapped_column(ForeignKey("MONITORES.id_usuario"))
    fecha_inicio: Mapped[DateTime] = mapped_column(DateTime)
    fecha_fin: Mapped[DateTime] = mapped_column(DateTime)
    estado: Mapped[str] = mapped_column(String(50))
    proposito: Mapped[str] = mapped_column(String(255))
    
    recurso: Mapped["Recursos"] = relationship("Recursos", back_populates="reservas")
    monitor: Mapped[Optional["Monitor"]] = relationship("Monitor", back_populates="reservas")
    
class Equipos_portatiles(Base):
    __tablename__ = "EQUIPOS_PORTATILES"
    id_recurso: Mapped[int] = mapped_column(ForeignKey("RECURSOS.id_recurso"), primary_key=True, autoincrement=True)
    modelo: Mapped[str] = mapped_column(String(100))
    sistema_operativo: Mapped[str] = mapped_column(String(50))
    
class Laboratorios(Base):
    __tablename__ = "LABORATORIOS"
    id_recurso: Mapped[int] = mapped_column(ForeignKey("RECURSOS.id_recurso"), primary_key=True, autoincrement=True)
    capacidad: Mapped[int] = mapped_column(Integer)
    software: Mapped[str] = mapped_column(String(255))
    ubicacion: Mapped[str] = mapped_column(String(100))
    
    recursos: Mapped[Optional["Recursos"]] = relationship("Recursos", back_populates="laboratorios")
    
class Prestamos(Base):
    __tablename__ = "PRESTAMOS"
    id_prestamo: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_reserva: Mapped[int] = mapped_column(ForeignKey("RESERVAS.id_reserva"))
    id_monitor_entrega: Mapped[int] = mapped_column(ForeignKey("MONITORES.id_usuario"))
    hora_entrega: Mapped[DateTime] = mapped_column(DateTime)
    hora_devolucion: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    estado_recepcion: Mapped[str] = mapped_column(String(50), nullable=True)
    
    monitor: Mapped[Optional["Monitor"]] = relationship("Monitor", back_populates="prestamos")
    
class Sanciones(Base):
    __tablename__ = "SANCIONES"
    id_sancion: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_usuario_estudiante: Mapped[int] = mapped_column(ForeignKey("USUARIOS.id_usuario"))
    id_prestamo: Mapped[int] = mapped_column(ForeignKey("PRESTAMOS.id_prestamo"))
    fecha_inicio: Mapped[DateTime] = mapped_column(DateTime)
    fecha_fin: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    motivo: Mapped[str] = mapped_column(String(255))
    estado: Mapped[str] = mapped_column(String(50))
    
