from enum import Enum
from pydantic import BaseModel, field_validator
from datetime import date


class GenreURLChoices(Enum):
    ROCK = 'rock'
    METAL = 'metal'
    POP_ROCK = 'pop rock'


class GenreChoices(Enum):
    ROCK = 'Rock'
    METAL = 'Metal'
    POP_ROCK = 'Pop Rock'


# se album não ficar em cima, vai apitar embaixo


class Album(BaseModel):
    title: str
    release_date: date


class BandBase(BaseModel):
    name: str
    genre: GenreChoices
    # valor default, se não tiver na saída mas não tiver default, dá erro
    albums: list[Album] = []


class BandCreate(BandBase):
    @field_validator('genre', mode='before')
    def title_case_genre(cls, value):
        return value.title()  # rock - Rock


class BandWithID(BandBase):
    id: int
