from sqlalchemy import create_engine, text
from typing import List
import config
from src.logger import get_logger


### Panggil logger dari logger.py untuk logging
logger = get_logger("loader")



## 1. Create Engine
engine = create_engine(config.DATABASE_URL)



## 2. Insert Data into Table (Data Film)
def load_films(transformed_films: List[dict]) -> None:
    # logging (start)
    logger.info("Starting film data loading")
    success = 0
    errors = 0

    # connect engine
    with engine.connect() as conn:
        # untuk setiap baris di data
        for data in transformed_films:
            try:
                # update dan insert data into table
                conn.execute(text("""
                        insert into film_transformed (film_id, title, description, release_year, rental_duration, 
                                                        rental_rate, film_length, rating, duration_category, is_premium)
                        values (:film_id, :title, :description, :release_year, :rental_duration, 
                                :rental_rate, :film_length, :rating, :duration_category, :is_premium)
                        on conflict (film_id)
                        do update set
                                title = excluded.title,
                                description = excluded.description,
                                release_year = excluded.release_year,
                                rental_duration = excluded.rental_duration,
                                rental_rate = excluded.rental_rate,
                                film_length = excluded.film_length,
                                rating = excluded.rating,
                                duration_category = excluded.duration_category,
                                is_premium = excluded.is_premium
                """), data)
                success += 1
            except Exception as e:
                # logging (error)
                logger.warning(f"Data: {data} skipped because error: {e}")
                errors += 1

        # logging (finish)
        logger.info(f"Loading complete: {success} success, {errors} errors")
        # commit engine
        conn.commit()



## 3. Insert Data into Table (Data Rental)
def load_rentals(transformed_rentals: List[dict]) -> None:
    # logging (start)
    logger.info("Starting rental data loading")
    success = 0
    errors = 0

    # connect engine
    with engine.connect() as conn:
        # untuk setiap baris
        for data in transformed_rentals:
            try:
                # update dan insert data into table
                conn.execute(text("""
                        insert into rental_transformed (rental_id, rental_date, inventory_id, customer_id,
                                                        return_date, staff_id, is_returned, rental_duration_days)
                        values (:rental_id, :rental_date, :inventory_id, :customer_id,
                                :return_date, :staff_id, :is_returned, :rental_duration_days)
                        on conflict (rental_id)
                        do update set
                                rental_date = excluded.rental_date,
                                inventory_id = excluded.inventory_id,
                                customer_id = excluded.customer_id,
                                return_date = excluded.return_date,
                                staff_id = excluded.staff_id,
                                is_returned = excluded.is_returned,
                                rental_duration_days = excluded.rental_duration_days
                """), data)
                success += 1
            except Exception as e:
                # logging (error)
                logger.warning(f"Data: {data} skipped because error: {e}")
                errors += 1
        
        # logging (finish)
        logger.info(f"Loading complete: {success} success, {errors} errors")
        # commit engine
        conn.commit()

