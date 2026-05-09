from sqlalchemy import create_engine, text
from typing import List
import config 
from src.logger import get_logger


# activate logging
logger = get_logger("loader")


# create engine
engine = create_engine(config.DATABASE_URL)

# create load function
def load_data(transformed_data: List[dict]) -> None:
    logger.info("Starting data loading")
    success = 0
    errors = 0

    with engine.connect() as conn:
        # DISINI, TIDAK PAKAI UPDATE INSERT (UPSERT) KARENA TIDAK ADA PRIMARY KEY
        # SETIAP KALI PIPELINE DI RUN, MAKA HARUS HAPUS ISI TABLE DULU AGAR DATA TIDAK DUPLIKAT
        # DAN RESTART ID SERIAL KEY KITA
        conn.execute(text("truncate table delayed_flights_clean restart identity"))

        for row in transformed_data:
            try:
                  conn.execute(text("""
                                    insert into delayed_flights_clean (Year, Month, DayofMonth,
                                          UniqueCarrier, FlightNum, Origin, Dest, Distance, 
                                          DistanceCategory, Cancelled, is_cancelled, CancellationCode, 
                                          CancellationReason, is_delayed, ArrDelay, DepDelay, 
                                          is_weather_delay, WeatherDelay, CarrierDelay, Diverted)
                                    values (:Year, :Month, :DayofMonth, :UniqueCarrier, :FlightNum, :Origin, 
                                          :Dest, :Distance, :DistanceCategory, :Cancelled, :is_cancelled, 
                                          :CancellationCode, :CancellationReason, :is_delayed, :ArrDelay, 
                                          :DepDelay, :is_weather_delay, :WeatherDelay, :CarrierDelay, :Diverted)
                                    """), row)
                  success += 1
            except Exception as e:
                 logger.warning(f"Row {row} skipped, because: {e}")
                 errors += 1

        logger.info(f"Loading complete: {success} success, {errors} errors")
        conn.commit()