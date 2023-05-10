import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie_routers import movie_router
from routers.user_router import user_router

# Para iniciar el servidor local usamos ==> uvicorn main:app --reload --port 5000 --host 0.0.0.0

app = FastAPI()  # Nombre de la aplicación
app.title = "Mi aplicación con FastAPI"  # Titulo de la documentación
app.version = "0.0.1"  # Version de la documentación

app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)

@app.get("/", tags=["home"])  # esta función devolver un Hello World"
def message():
    return HTMLResponse("<h1>Hello world</h1>")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0",
                port=int(os.environ.get("PORT", 8000)))