# test_db_connection.py
import sys
import os

sys.path.insert(
    0,
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
)

from sqlalchemy import text
from infraestructure.database import engine, sesionLocal, DATABASE_URL


def test_db_connection():
    print(f"Intentando conectar a: {DATABASE_URL}\n")

    # 1. probar el engine directamente
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM ROLES"))

            print("Conexión al motor de base de datos exitosa.")
            print(f"Resultado SELECT 1: {result.fetchone()}")

    except Exception as e:
        print(f"Error al conectar con el motor de base de datos: {e}")
        return

    print("\nTodas las pruebas pasaron. La BD está operativa.")


test_db_connection()