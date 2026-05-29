#Este es el archivo principal del proyecto, entrada principal de nuestro proyecto

#para ejecutar la aplicacion desde la consola debemos ejecutar la siguiente linea
# venv\Scripts\uvicorn.exe main:app --reload

#la documentacion interactiva queda disponible
# http://localhost:8000/docs swagger UI (recomendado para probar)
# http://localhost:8000/redoc Redoc (documentacion alternativa)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.route import router, alias_router

app = FastAPI(
    title="IUTEDE - Gestion de TICS",
    description="Api para la gestion de los recursos TICs de la UTEDE",
    version="1.0.0"
)

#Middleware CORS permited que el front (react, VUE) pueda hacer peticiones a esta API, el cors es como una capa de seguridad
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

#Registrar todas las rutas definidas en el archivo route.py
app.include_router(router)
app.include_router(alias_router)

#endpoint de salud, para ver si la api esta funcionando o no
@app.get("/",tags=["Health salud check"])
def health_check():
    return{"Status": "ok", "api": "IUTEDE Backend", "Version": "1.0.0"}
