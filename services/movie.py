from models.movie import Movie as MovieModel
from schemas.movie import Movie

class MovieServices():

    def __init__(self, db) -> None:
        self.db = db

    def get_movies(self):
        result = self.db.query(MovieModel).all()
        return result

    def get_movie_id(self, id):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return result

    def get_movie_category(self, category):
        result = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return result

    def create_movie(self, movie: Movie):
        new_movie = MovieModel(**movie.dict())
        self.db.add(new_movie)
        self.db.commit()
        return

    def update_movie(self, id: int, data: Movie):
        movie = self.get_movie_id(id)
        movie.title = data.title or movie.title
        movie.overview = data.overview or movie.overview
        movie.year = data.year or movie.year
        movie.rating = data.rating or movie.rating
        movie.category = data.category or movie.category
        self.db.commit()
        return

    def check_duplicate_movie(self, movie):
        check_movie = self.db.query(MovieModel).filter(MovieModel.title == movie.title, MovieModel.year == movie.year).all()
        return check_movie

    def delete_movie(self, id: int):
        delete_movie = self.get_movie_id(id)
        self.db.delete(delete_movie)
        self.db.commit()
        return