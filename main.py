#https://www.youtube.com/watch?v=Lw-zLopB3o0&list=PL-2EBeDYMIbQghmnb865lpdmYyWU3I5F1

from fastapi import FastAPI, HTTPException
from enum import Enum

app = FastAPI()

class GenreURLChoices(Enum):
    ROCK = 'rock'
    METAL = 'metal'
    POP_ROCK = 'pop rock'

BANDS = [
    {'id':1, 'name': 'Iron Maiden', 'genre': 'Rock',},
    {'id':2, 'name': 'Metallica', 'genre': 'Metal',},
    {'id':3, 'name': 'Pink Floyd', 'genre': 'Progressive Rock',},
    {'id':4, 'name': 'Led Zeppelin', 'genre': 'Hard Rock',},
    {'id':5, 'name': 'The Beatles', 'genre': 'Pop Rock',},
    {'id':6, 'name': 'AC/DC', 'genre': 'Rock'}
]

@app.get('/bands')
async def bands() -> list[dict]:

    return BANDS

@app.get('/bands/{band_id}', status_code=206)
async def band(band_id: int) -> dict:
    band = next((b for b in BANDS if b['id'] == band_id), None)

    if band is None:
        raise HTTPException(status_code=404, detail='Band not fund')

    return band

@app.get('/bands/genre/{genre}')
async def bands_for_genre(genre:GenreURLChoices) -> list[dict]:

    return [
        b for b in BANDS if b['genre'].lower() == genre.value
    ]



@app.get('/about')
# o tipo tem que ser correto
async def about() -> str:
    return 'A great company'