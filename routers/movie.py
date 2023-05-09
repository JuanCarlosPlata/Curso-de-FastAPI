from fastapi import APIRouter
from fastapi import Depends, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from middlewares.jwt_bearer import JWTBearer
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from schemas.movie import Movie, Update_Movie
from services.movie import MovieServices


movie_router = APIRouter()


@movie_router.get("/movies", tags=["movies"], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    # In Python, -> is used to indicate the return type of a function.
    db = Session()
    result = MovieServices(db).get_movies()
    return JSONResponse(content=jsonable_encoder(result))

# Filtrado de películas por id


@movie_router.get("/movies/{id}", tags=["movies"], response_model=Movie, status_code=200)
def get_movies_by_id(id: int = Path(ge=1, le=1000)) -> Movie:
    # In Python, -> is used to indicate the return type of a function.
    db = Session()
    # Comprobar si la película con el id se encuentra en la lista de películas
    # el .first sirve para que que se detenga y devuelva el primer valor que coincida con el id
    result = MovieServices(db).get_movie_id(id)
    if not result:  # se muestra el HTTPException cuando no se encuentra el id de la película
        raise HTTPException(
            status_code=404, detail=f"No movie found with id {id}")
    return JSONResponse(content=jsonable_encoder(result))

# Filtrar película por categoría


@movie_router.get("/movies/", tags=["movies"], response_model=List[Movie], status_code=200)
def get_movies_by_category(category: str = Query(min_length=4, max_length=15)) -> List[Movie]:
    # In Python, -> is used to indicate the return type of a function.
    db = Session()
    # Comprobar si la categoría se encuentra en la lista de películas
    result = MovieServices(db).get_movie_category(category)
    # usamos .all para que me muestre todas las películas que coincidan con la categoría deseada
    if not result:
        # se muestra el HTTPException cuando no se encuentra la categoría de película
        raise HTTPException(
            status_code=404, detail=f"No movies found with category {category}")
    # se retornaran todas las películas que coincidan con la categoría deseada
    return JSONResponse(content=jsonable_encoder(result))

# Crear una nueva película


@movie_router.post("/movies", tags=["movies"], response_model=dict, status_code=200)
def create_movie(movie: Movie) -> dict:
    # In Python, -> is used to indicate the return type of a function.
    db = Session()
    # se buscara en la base de datos si la combinación de title y year ya se encuentran en la base de datos
    result = MovieServices(db).check_duplicate_movie(movie)
    if result:  # si encuentra que el titulo y el año de la nueva película ya existe en la base de datos levantara un HTTPException
        raise HTTPException(
            status_code=404, detail=f"Movie with title {movie.title} and year {movie.year} already exists")
    # si la combinación de titulo y año de la nueva película no esta en la base de datos (es posible que tengan el mismo titulo pero no el año ya que puede ser una nueva version de la misma película) se creara la nueva película
    else:
        MovieServices(db).create_movie(movie)
        # Mensaje que indica que se creo exitosamente la película
        return JSONResponse(content={"message": "Se ha creado la película"})


# Actualizar datos de una película


@movie_router.put("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
def update_movie(id: int, movie: Update_Movie) -> dict:
    # In Python, -> is used to indicate the return type of a function.
    # si no encuentra el id devolverá None
    db = Session()
    result = MovieServices(db).get_movie_id(id)
    if not result:  # se muestra el HTTPException cuando no se encuentra el id de la película
        raise HTTPException(
            status_code=404, detail=f"No movie found with id {id}")
    # se modificara la película con los nuevos datos o si no se introducen nuevos datos se mantendrán los datos anteriores
    MovieServices(db).update_movie(id, movie)
    return JSONResponse(content={"message": f"Se ha modificado la película {result.title} con el id {id}"})


# Eliminar una película


@movie_router.delete("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    # In Python, -> is used to indicate the return type of a function.
    db = Session()
    result = MovieServices(db).get_movie_id(id)
    if not result:  # se muestra el HTTPException cuando no se encuentra el id de la película
        raise HTTPException(
            status_code=404, detail=f"No movie found with id {id}")
    MovieServices(db).delete_movie(id)
    return JSONResponse(content={"message": f"Se ha eliminado la película {result.title} con el id {id}"})