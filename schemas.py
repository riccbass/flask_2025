from enum import Enum
from pydantic import BaseModel
from datetime import date


class GenreURLChoices(Enum):
    ROCK = 'rock'
    METAL = 'metal'
    POP_ROCK = 'pop rock'

# se album não ficar em cima, vai apitar embaixo


class Album(BaseModel):

    title: str
    release_date: date


class Band(BaseModel):

    # {'id':1, 'name': 'Iron Maiden', 'genre': 'Rock',},
    id: int
    name: str
    genre: str
    # valor default, se não tiver na saída mas não tiver default, dá erro
    albums: list[Album] = []
