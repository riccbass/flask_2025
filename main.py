# https://www.youtube.com/watch?v=Lw-zLopB3o0&list=PL-2EBeDYMIbQghmnb865lpdmYyWU3I5F1

from fastapi import FastAPI, HTTPException
from schemas import GenreURLChoices, BandBase, BandCreate, BandWithID

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
# se não no url da rota mas tá no parâmetro, é query param ?
# se tem o query parameter, precisa do default caso contrário vai dar erro
async def bands(genre: GenreURLChoices | None = None,
                has_albums: bool = False
                ) -> list[BandWithID]:

    band_list = [BandWithID(**b) for b in BANDS]

    if genre:
        band_list = [
            b for b in band_list if b.genre.value.lower() == genre.value
        ]

    if has_albums:

        band_list = [b for b in band_list if len(b.albums) > 0]

    return band_list


@app.get('/bands/{band_id}', status_code=206)
async def band(band_id: int) -> BandWithID:
    band = next((BandWithID(**b) for b in BANDS if b['id'] == band_id), None)

    if band is None:
        raise HTTPException(status_code=404, detail='Band not fund')

    return band


@app.get('/about')
# o tipo tem que ser correto
async def about() -> str:
    return 'A great company'


@app.post("/bands")
async def create_band(band_data: BandCreate) -> BandWithID:

    id = BANDS[-1]['id'] + 1
    band = BandWithID(id=id, **band_data.model_dump())
    BANDS.append(band.model_dump())

    return band
