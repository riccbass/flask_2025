# https://www.youtube.com/watch?v=Lw-zLopB3o0&list=PL-2EBeDYMIbQghmnb865lpdmYyWU3I5F1

from fastapi import FastAPI, HTTPException
from schemas import GenreURLChoices, Band

app = FastAPI()

BANDS = [
    {
        'id': 1,
        'name': 'Iron Maiden',
        'genre': 'Rock',
        'albums': [
            {
                'title': 'Iron Maiden',
                'release_date': '1971-07-21'
            },
            {
                'title': 'Killers',
                'release_date': '1980-06-12',
            }
        ]
    },
    {
        'id': 2,
        'name': 'Metallica',
        'genre': 'Metal'
    },
    {
        'id': 3,
        'name': 'Pink Floyd',
        'genre': 'Progressive Rock'
    },
    {
        'id': 4,
        'name': 'Led Zeppelin',
        'genre': 'Hard Rock'
    },
    {
        'id': 5,
        'name': 'The Beatles',
        'genre': 'Pop Rock'
    },
    {
        'id': 6,
        'name': 'AC/DC',
        'genre': 'Rock'
    }
]


@app.get('/bands')
# a vantagem de usar o pydantic é que já valida a data
async def bands() -> list[Band]:

    return [
        Band(**b) for b in BANDS
    ]


@app.get('/bands/{band_id}', status_code=206)
async def band(band_id: int) -> Band:
    band = next((Band(**b) for b in BANDS if b['id'] == band_id), None)

    if band is None:
        raise HTTPException(status_code=404, detail='Band not fund')

    return band


@app.get('/bands/genre/{genre}')
async def bands_for_genre(genre: GenreURLChoices) -> list[dict]:

    return [
        b for b in BANDS if b['genre'].lower() == genre.value
    ]


@app.get('/about')
# o tipo tem que ser correto
async def about() -> str:
    return 'A great company'
