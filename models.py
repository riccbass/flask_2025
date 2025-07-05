from enum import Enum
from pydantic import BaseModel, field_validator
from datetime import date
from sqlmodel import SQLModel, Field, Relationship


class GenreURLChoices(Enum):
    ROCK = 'rock'
    METAL = 'metal'
    POP_ROCK = 'pop rock'


class GenreChoices(Enum):
    ROCK = 'Rock'
    METAL = 'Metal'
    POP_ROCK = 'Pop Rock'

# ------------------------------------------------------------------------
# Modelos SQLModel/Pydantic - Organização das Classes
#
# Cada classe tem um papel específico:
#
#   Classe         | Finalidade principal
# -----------------|------------------------------------------------------
#   BandBase       | Define campos comuns que toda banda tem (evita repetição).
#   Band           | Modelo completo do banco de dados, usado em queries/ORM.
#   BandCreate     | Modelo de entrada da API, usado ao criar uma nova banda.
#   AlbumBase      | Define campos comuns de todo álbum (evita repetição).
#   Album          | Modelo persistente com table=True, com id e relações.
#   AlbumCreate    | Modelo de entrada usado na criação de um álbum.
# ------------------------------------------------------------------------


class AlbumBase(SQLModel):
    title: str
    release_date: date
    band_id: int | None = Field(foreign_key="band.id")

    @field_validator('release_date', mode='before')
    def parse_date(cls, value):
        if isinstance(value, str):
            from datetime import datetime
            return datetime.strptime(value, '%Y-%m-%d').date()
        return value


class Album(AlbumBase, table=True):
    id: int = Field(default=None, primary_key=True)
    band: "Band" = Relationship(back_populates="albums")


class AlbumCreate(SQLModel):
    title: str
    release_date: date

    @field_validator('release_date', mode='before')
    def parse_date(cls, value):
        if isinstance(value, str):
            from datetime import datetime
            return datetime.strptime(value, '%Y-%m-%d').date()
        return value

# É um padrão comum: separar modelos de entrada (API) dos modelos de banco!


class BandBase(SQLModel):
    name: str
    genre: GenreChoices
    # valor default, se não tiver na saída mas não tiver default, dá erro


# O SQLModel automaticamente mantém a consistência -
# quando você adiciona um album a uma banda,
# o album automaticamente "sabe" qual é sua banda,
# e vice-versa.
# O back_populates é essencial para criar relacionamentos eficientes e evitar consultas desnecessárias ao banco de dados!


class Band(BandBase, table=True):
    id: int = Field(default=None, primary_key=True)
    albums: list[Album] = Relationship(back_populates="band")


class BandCreate(BandBase):
    albums: list[AlbumCreate] | None = None

    @field_validator('genre', mode='before')
    def title_case_genre(cls, value):
        return value.title()  # rock - Rock
