from uuid import UUID

from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository



class InMemoryGenreRepository(GenreRepository):
    def __init__(self, genres=None):
        self.genres = genres or []

    def save(self, genre) -> None:
        self.genres.append(genre)

    def get_by_id(self, id: UUID) -> Genre:
        for genre in self.genres:
            if genre.id == id:
                return genre
        return None

    def delete(self, id: UUID) -> None:
        for genre in self.genres:
            if genre.id == id:
                self.genres.remove(genre)
                return
        return None
    
    def update(self, genre: Genre) -> None:
        old_genre = self.get_by_id(genre.id)
        if old_genre:
            self.genres.remove(old_genre)
            self.genres.append(genre)
            
    def list(self) -> list[Genre]:
        return self.genres
    
