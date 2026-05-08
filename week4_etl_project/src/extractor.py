import pandas as pd
import numpy as np
from pathlib import Path
from typing import List
from src.models import FilmRecord, RentalRecord
from src.logger import get_logger
import config


## 1. Panggil Data
FILM_CSV = "data/raw/film.csv"
RENTAL_CSV = "data/raw/rental.csv"

# atau bisa dengan memanggil dari config, karena sudah kita tulis di config
FILM_CSV = config.FILM_CSV
RENTAL_CSV = config.RENTAL_CSV


## 2. Panggil Logger dari File logger.py untuk Logging
logger = get_logger("extractor")


## 2. Extract Data in film.csv Using Validator Model
def extract_films() -> List[FilmRecord]:        #menunjukkan output fungsi ini adalah list yang isinya hanya boleh objek dari FilmRecord
    # logging (start)
    logger.info("Starting film data extraction")

    data_film = pd.read_csv(FILM_CSV)           #data terdiri dari index, data
    data_film = data_film.replace({np.nan: None})       #replace NaN with None
    films = []
    errors = 0

    for index, data in data_film.iterrows():        #untuk setiap row nya
        try:
            films.append(FilmRecord(**data.to_dict()))  #data berbentuk Series, maka ubah ke dictionary, dan unpack dict
        except Exception as e:
            # logging (error)
            logger.warning(f"Row {index} skipped because error: {e}")
            errors += 1
    
    # logging (finish)
    logger.info(f"Extraction complete: {len(films)} success, {errors} errors")
    return films


## 3. Extract Data in rental.csv Using Validator Model 
def extract_rentals() -> List[RentalRecord]:
    # logging start
    logger.info("Starting rental data extraction")

    data_rental = pd.read_csv(RENTAL_CSV)
    data_rental = data_rental.replace({np.nan: None})
    rentals = []
    errors = 0

    for index, data in data_rental.iterrows():
        try:
            rentals.append(RentalRecord(**data.to_dict()))
        except Exception as e:
            # logging error
            logger.warning(f"Row {index} skipped because error: {e}")
            errors += 1
    
    # logging finish
    logger.info(f"Extraction complete: {len(rentals)} success, {errors} errors")
    return rentals





#### CHECK APAKAH BERHASIL DI TERMINAL
## python -c "from src.extractor import extract_films, extract_rentals; films = extract_films(); rentals = extract_rentals(); print(f'Films: {len(films)}, Rentals: {len(rentals)}')"