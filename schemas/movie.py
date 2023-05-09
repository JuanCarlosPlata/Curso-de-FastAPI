
#clase creada para ser usada al momento de actualizar películas
import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Update_Movie(BaseModel):
    # Modelo de película con campos de título, descripción general,
    # año, calificación y categoría. Los campos tienen restricciones y validaciones.
    id: Optional[int] = None
    title: str = Field(max_length=15)
    overview: str = Field(max_length=50)
    year: int = Field(le=datetime.date.today().year)
    rating: float = Field(le=10)
    category: str = Field(max_length=15)

    class Config():
        # Configuración adicional para proporcionar un ejemplo de datos para el modelo
        schema_extra = {
            "example":{
                "title": "",
                "overview": "",
                "year": 0,
                "rating": 0,
                "category": ""
            }
        }

class Movie(BaseModel):
    # Modelo de película con campos de id, título, descripción general,
    # año, calificación y categoría. Los campos tienen restricciones y validaciones.
    id: Optional[int] = None # teniendo este parámetro como optional la base de datos genera el id automáticamente
    title: str = Field(min_length=4, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=datetime.date.today().year)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=4, max_length=15)

    class Config():
        # Configuración adicional para proporcionar un ejemplo de datos para el modelo
        schema_extra = {
            "example":{
                "title": "Nombre de película",
                "overview": "Descripción de la película",
                "year": 2023,
                "rating": 5.0,
                "category": "Categoría de la película"
            }
        }