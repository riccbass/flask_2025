# https://www.youtube.com/watch?v=Lw-zLopB3o0&list=PL-2EBeDYMIbQghmnb865lpdmYyWU3I5F1

from fastapi import FastAPI, HTTPException, Depends
from models import GenreURLChoices, BandBase, BandCreate, Band, Album
from typing import Annotated
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from db import init_db, get_session

from datetime import datetime


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get('/bands')
# a vantagem de usar o pydantic é que já valida a data
# se não no url da rota mas tá no parâmetro, é query param ?
# se tem o query parameter, precisa do default caso contrário vai dar erro
async def bands(genre: GenreURLChoices | None = None,
                has_albums: bool = False,
                session: Session = Depends(get_session)
                ) -> list[Band]:

    # ele pede para converter para lista
    band_list = list(session.exec(select(Band)).all())

    if genre:
        band_list = [
            b for b in band_list if b.genre.value.lower() == genre.value
        ]

    if has_albums:

        band_list = [b for b in band_list if len(b.albums) > 0]

    return band_list


@app.get('/bands/{band_id}', status_code=206)
async def band(band_id: int, session: Session = Depends(get_session)) -> Band:

    band = session.get(Band, band_id)

    if band is None:
        raise HTTPException(status_code=404, detail='Band not fund')

    return band


@app.post("/bands")
async def create_band(
    band_data: BandCreate,
    session: Session = Depends(get_session)
) -> Band:

    band = Band(name=band_data.name, genre=band_data.genre)
    session.add(band)

    if band_data.albums:
        for album in band_data.albums:

            album_obj = Album(
                title=album.title, release_date=album.release_date, band=band, band_id=None
            )

            session.add(album_obj)

    session.commit()
    # com esse refresh já pega os dadaos do banco, com id
    session.refresh(band)

    return band
