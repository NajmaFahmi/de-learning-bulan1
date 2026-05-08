from typing import List, Optional
from src.models import FilmRecord, RentalRecord
from src.logger import get_logger



## Panggil logger dari file logger.py untuk logging
logger = get_logger("transformer")



## A. Transform Data film.csv
def transform_films(films: List[FilmRecord]) -> List[dict]:
    # logging (start)
    logger.info("Starting film data transformation")

    transformed_films = []
    errors = 0

    for row in films:
        try:
            # convert data (filmrecord object) into dict
            data = row.model_dump()

            # categorize film duration
            if data['length'] < 60:
                data['duration_category'] = "Short"
            elif data['length'] < 120:
                data['duration_category'] = "Medium"
            else:
                data['duration_category'] = "Long"
            
            # normalize rating
            data['rating'] = data['rating'].upper().strip()

            # categorize film rental_rate
            if data['rental_rate'] >= 3.99:
                data['is_premium'] = True
            else:
                data['is_premium'] = False
            
            # convert rental_rate from Decimal to str (python sulit pass Decimal ke sql)
            data['rental_rate'] = str(data['rental_rate'])

            # rename kolom 'length'
            data['film_length'] = data.pop('length')

            # add transformed data into list
            transformed_films.append(data)

        except Exception as e:
            # logging (error)
            logger.warning(f"Data: {row} skipped because error: {e}")
            errors += 1

    # logging (finish)
    logger.info(f"Transformation complete: {len(transformed_films)} success, {errors} errors")
    # return list[dict]
    return transformed_films



## B. Transform Data rental.csv
def transform_rentals(rentals: List[RentalRecord]) -> List[dict]:
    # logging (start)
    logger.info("Starting rental data transformation")

    transformed_rentals = []
    errors = 0

    for row in rentals:
        try:
            # convert data (rentalrecord object) into dict
            data = row.model_dump()

            # check if rentaled film already return or not
            # and count rental_duration_days
            if data['return_date'] is None:
                data['is_returned'] = False
                data['rental_duration_days'] = None
            else:
                data['is_returned'] = True
                data['rental_duration_days'] = (data['return_date'] - data['rental_date']).days
            
            # add transformed data into list
            transformed_rentals.append(data)

        except Exception as e:
            # logging (error)
            logger.warning(f"Data: {row} skipped because error: {e}")
            errors += 1
    
    # logging (finish)
    logger.info(f"Transformation complete: {len(transformed_rentals)} success, {errors} errors")
    # return list[dict]
    return transformed_rentals
