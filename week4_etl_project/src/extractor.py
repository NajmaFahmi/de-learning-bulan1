import pandas as pd
import numpy as np
from pathlib import Path
from typing import List
from src.models import FilmRecord, RentalRecord
import config


## 1. Buat Variable
FILM_CSV = "data/raw/film.csv"
RENTAL_CSV = "data/raw/rental.csv"


## 2. Extract Data in film.csv Using Validator Model
def extract_films() -> List[FilmRecord]:
    data_film = pd.read_csv(FILM_CSV)
    data_film = data_film.replace({np.nan: None})
    films = []
    for index, data in data_film.iterrows():
        films.append(FilmRecord(**data.to_dict()))
    return films


## 3. Extract Data in rental.csv Using Validator Model 
def extract_rentals() -> List[RentalRecord]:
    data_rental = pd.read_csv(RENTAL_CSV)
    data_rental = data_rental.replace({np.nan: None})
    rentals = []
    for index, data in data_rental.iterrows():
        rentals.append(RentalRecord(**data.to_dict()))
    return rentals